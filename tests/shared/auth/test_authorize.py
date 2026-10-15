import pytest

from app.shared.auth.authorize import authenticate, authorize_user
from app.shared.clients.cognito import CognitoClient
from app.shared.errors import UnauthenticatedError
from tests.fixtures.api import CognitoUsers


class TestAuthorizeUser:
    def test_yields_the_caller(self, cognito_users: CognitoUsers, cognito: CognitoClient) -> None:
        token = cognito_users.sign_in("a@x.io")

        with authorize_user({"authorization": f"Bearer {token}"}) as user:
            assert user.id == cognito.get_user(token)["Username"]

    @pytest.mark.usefixtures("cognito")
    @pytest.mark.parametrize("header", [None, "", "Bearer", "Basic abc", "Bearer not-a-token"])
    def test_rejects_missing_or_invalid_header(self, header: str | None) -> None:
        with pytest.raises(UnauthenticatedError):
            authenticate(header)
