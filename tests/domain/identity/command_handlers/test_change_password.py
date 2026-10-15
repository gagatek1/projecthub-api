import pytest
from pydantic import SecretStr

from app.domain.identity.command_handlers.change_password import change_password_handler
from app.domain.identity.command_handlers.sign_in import sign_in_handler
from app.domain.identity.commands.change_password import ChangePasswordCommand
from app.domain.identity.commands.sign_in import SignInCommand
from app.domain.identity.exceptions import InvalidCredentialsError
from tests.fixtures.api import CognitoUsers

NEW_PASSWORD = "N3wPassw0rd!"

PASSWORD = "Passw0rd!x"


class TestChangePasswordHandler:
    def test_changes_password(self, cognito_users: CognitoUsers) -> None:
        token = cognito_users.sign_in("a@x.io", PASSWORD)

        change_password_handler(
            ChangePasswordCommand(access_token=SecretStr(token), old_password=PASSWORD, new_password=NEW_PASSWORD)
        )

        assert sign_in_handler(SignInCommand(email="a@x.io", password=NEW_PASSWORD)).access_token

    def test_wrong_old_password(self, cognito_users: CognitoUsers) -> None:
        token = cognito_users.sign_in("a@x.io", PASSWORD)

        with pytest.raises(InvalidCredentialsError):
            change_password_handler(
                ChangePasswordCommand(
                    access_token=SecretStr(token), old_password="Wrong0ld!x", new_password=NEW_PASSWORD
                )
            )
