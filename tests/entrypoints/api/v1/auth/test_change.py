import pytest
from fastapi.testclient import TestClient

from app.shared.clients.cognito import CognitoClient
from tests.fixtures.api import Tokens
from tests.fixtures.aws import CognitoFailure

BODY = {"old_password": "Passw0rd!x", "new_password": "N3wPassw0rd!"}


class TestChangePasswordEndpoint:
    def test_changes_password_with_callers_token(
        self, client: TestClient, tokens: Tokens, cognito: CognitoClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        calls: list[tuple[str, ...]] = []
        monkeypatch.setattr(cognito, "change_password", lambda *args: calls.append(args))

        assert client.post("/api/v1/auth/change", json=BODY, headers=tokens.of("alice")).status_code == 200
        assert calls == [("token-alice", "Passw0rd!x", "N3wPassw0rd!")]

    def test_wrong_old_password_is_401(self, client: TestClient, tokens: Tokens, cognito_error: CognitoFailure) -> None:
        cognito_error("change_password", "NotAuthorizedException")

        assert client.post("/api/v1/auth/change", json=BODY, headers=tokens.of("alice")).status_code == 401
