import pytest

from app.shared.pagination import InvalidCursorError, decode_cursor, encode_cursor

KEY = {"pk": {"S": "project"}, "sk": {"S": "project#1"}}


class TestPagination:
    def test_round_trip(self) -> None:
        assert decode_cursor(encode_cursor(KEY), pk="project") == KEY

    def test_no_cursor(self) -> None:
        assert encode_cursor(None) is None
        assert decode_cursor(None, pk="project") is None

    @pytest.mark.parametrize(
        "cursor",
        [
            "not-base64!",
            "x" * 3000,
            encode_cursor({"pk": {"S": "project#other"}, "sk": {"S": "x"}}),
            encode_cursor({"pk": {"N": "1"}, "sk": {"S": "x"}}),
            encode_cursor({**KEY, "extra": {"S": "y"}}),
        ],
    )
    def test_rejects_tampered_cursor(self, cursor: str) -> None:
        with pytest.raises(InvalidCursorError):
            decode_cursor(cursor, pk="project")
