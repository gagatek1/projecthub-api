import boto3
import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.domain.identity.query_service import UserQueryService
from app.entrypoints.api.api_gateway_handler import app
from app.shared.auth import authorize
from app.shared.auth.authorize import AuthUser
from app.shared.clients.cognito import CognitoClient
from app.shared.errors import UnauthenticatedError


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


class Tokens:
    def __init__(self) -> None:
        self._users: dict[str, AuthUser] = {}

    def of(self, user_id: str) -> dict[str, str]:
        token = f"token-{user_id}"
        self._users[token] = AuthUser(id=user_id, sub=None, access_token=SecretStr(token))
        return {"Authorization": f"Bearer {token}"}

    def authenticate(self, authorization: str | None) -> AuthUser:
        scheme, _, token = (authorization or "").partition(" ")
        if scheme.lower() != "bearer" or token not in self._users:
            raise UnauthenticatedError
        return self._users[token]


@pytest.fixture
def tokens(monkeypatch: pytest.MonkeyPatch) -> Tokens:
    mock = Tokens()
    monkeypatch.setattr(authorize, "authenticate", mock.authenticate)
    return mock


@pytest.fixture
def known_users(monkeypatch: pytest.MonkeyPatch) -> set[str]:
    users = {"alice", "bob"}
    monkeypatch.setattr(UserQueryService, "user_exists", lambda _, username: username in users)
    return users


class CognitoUsers:
    def __init__(self, cognito: CognitoClient) -> None:
        self._cognito = cognito

    def sign_in(self, email: str, password: str = "Passw0rd!x") -> str:
        self._cognito.sign_up(email, password)
        boto3.client("cognito-idp", region_name="eu-central-1").admin_confirm_sign_up(
            UserPoolId=self._cognito._user_pool_id, Username=email
        )
        result = self._cognito.initiate_auth("USER_PASSWORD_AUTH", email, {"USERNAME": email, "PASSWORD": password})
        return result["AccessToken"]


@pytest.fixture
def cognito_users(cognito: CognitoClient) -> CognitoUsers:
    return CognitoUsers(cognito)
