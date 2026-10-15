import pytest
from fastapi.testclient import TestClient

from app.shared.clients.cognito import CognitoClient
from tests.fixtures.api import Tokens


class TestUpdateEmailEndpoint:
    def test_sends_change_with_callers_token(
        self, client: TestClient, tokens: Tokens, cognito: CognitoClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        calls: list[tuple[str, str]] = []
        monkeypatch.setattr(cognito, "update_email", lambda token, email: calls.append((token, email)))

        response = client.put("/api/v1/users/me/email", json={"email": "new@x.io"}, headers=tokens.of("alice"))

        assert response.status_code == 202
        assert calls == [("token-alice", "new@x.io")]

    def test_rejects_invalid_email(self, client: TestClient, tokens: Tokens) -> None:
        assert (
            client.put("/api/v1/users/me/email", json={"email": "nope"}, headers=tokens.of("alice")).status_code == 422
        )
