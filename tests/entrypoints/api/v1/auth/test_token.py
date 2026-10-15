import pytest
from fastapi.testclient import TestClient

from app.shared.clients.cognito import CognitoClient
from tests.fixtures.aws import CognitoFailure

BODY = {"user_id": "alice", "refresh_token": "r"}


class TestTokenEndpoint:
    def test_refreshes_access_token(
        self, client: TestClient, cognito: CognitoClient, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setattr(cognito, "initiate_auth", lambda *_: {"AccessToken": "a", "ExpiresIn": 3600})

        assert client.post("/api/v1/auth/token", json=BODY).json() == {"AccessToken": "a", "ExpiresIn": 3600}

    def test_invalid_refresh_token_is_401(self, client: TestClient, cognito_error: CognitoFailure) -> None:
        cognito_error("initiate_auth", "NotAuthorizedException")

        assert client.post("/api/v1/auth/token", json=BODY).status_code == 401
