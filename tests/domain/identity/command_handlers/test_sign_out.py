import pytest
from pydantic import SecretStr

from app.domain.identity.command_handlers.sign_out import sign_out_handler
from app.domain.identity.commands.sign_out import SignOutCommand
from app.shared.auth.authorize import authenticate
from app.shared.errors import UnauthenticatedError
from tests.fixtures.api import CognitoUsers

PASSWORD = "Passw0rd!x"


class TestSignOutHandler:
    def test_revokes_access_token(self, cognito_users: CognitoUsers) -> None:
        token = cognito_users.sign_in("a@x.io", PASSWORD)

        sign_out_handler(SignOutCommand(access_token=SecretStr(token)))

        with pytest.raises(UnauthenticatedError):
            authenticate(f"Bearer {token}")
