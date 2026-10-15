import base64
import binascii
import json
from typing import Any

from app.shared.errors import InvalidInputError

KEY_ATTRIBUTES = frozenset({"pk", "sk"})
MAX_CURSOR_LENGTH = 2048


class InvalidCursorError(InvalidInputError):
    default_message = "Invalid cursor"


def encode_cursor(last_evaluated_key: dict[str, Any] | None) -> str | None:
    if not last_evaluated_key:
        return None
    return base64.urlsafe_b64encode(json.dumps(last_evaluated_key, separators=(",", ":")).encode()).decode()


def decode_cursor(cursor: str | None, *, pk: str) -> dict[str, Any] | None:
    if cursor is None:
        return None
    try:
        if len(cursor) > MAX_CURSOR_LENGTH:
            raise ValueError
        key = json.loads(base64.urlsafe_b64decode(cursor.encode()))
    except (ValueError, binascii.Error) as exc:
        raise InvalidCursorError from exc
    if not _is_table_key(key) or key["pk"]["S"] != pk:
        raise InvalidCursorError
    return key


def _is_table_key(key: object) -> bool:
    return (
        isinstance(key, dict)
        and set(key) == KEY_ATTRIBUTES
        and all(isinstance(v, dict) and set(v) == {"S"} and isinstance(v["S"], str) for v in key.values())
    )
