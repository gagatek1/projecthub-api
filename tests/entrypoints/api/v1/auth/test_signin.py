import pytest
from fastapi.testclient import TestClient

from app.shared.clients.cognito import CognitoClient
from tests.fixtures.aws import CognitoFailure

BODY = {"email": "d@x.io", "password": "Passw0rd!x"}


class TestSigninEndpoint:
    def test_returns_tokens(self, client: TestClient, cognito: CognitoClient, monkeypatch: pytest.MonkeyPatch) -> None:
        result = {"AccessToken": "a", "RefreshToken": "r", "ExpiresIn": 3600}
        monkeypatch.setattr(cognito, "initiate_auth", lambda *_: result)

        response = client.post("/api/v1/auth/signin", json=BODY)

        assert response.json() == result

    @pytest.mark.parametrize(
        ("code", "status"),
        [("UserNotConfirmedException", 403), ("UserNotFoundException", 401), ("NotAuthorizedException", 401)],
    )
    def test_maps_errors(self, client: TestClient, cognito_error: CognitoFailure, code: str, status: int) -> None:
        cognito_error("initiate_auth", code)

        assert client.post("/api/v1/auth/signin", json=BODY).status_code == status
