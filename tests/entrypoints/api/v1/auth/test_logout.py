import pytest
from fastapi.testclient import TestClient

from app.shared.clients.cognito import CognitoClient
from tests.fixtures.api import Tokens


class TestLogoutEndpoint:
    def test_signs_out_globally_with_callers_token(
        self, client: TestClient, tokens: Tokens, cognito: CognitoClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        calls: list[str] = []
        monkeypatch.setattr(cognito, "global_sign_out", calls.append)

        assert client.post("/api/v1/auth/logout", headers=tokens.of("alice")).status_code == 204
        assert calls == ["token-alice"]
