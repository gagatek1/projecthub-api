import pytest

from app.domain.identity.command_handlers.sign_in import sign_in_handler
from app.domain.identity.command_handlers.sign_up import sign_up_handler
from app.domain.identity.commands.sign_in import SignInCommand
from app.domain.identity.commands.sign_up import SignUpCommand
from app.domain.identity.exceptions import AccountNotConfirmedError, InvalidCredentialsError
from app.shared.auth.authorize import authenticate
from tests.fixtures.api import CognitoUsers

PASSWORD = "Passw0rd!x"


class TestSignInHandler:
    def test_returns_tokens(self, cognito_users: CognitoUsers) -> None:
        cognito_users.sign_in("a@x.io", PASSWORD)

        tokens = sign_in_handler(SignInCommand(email="a@x.io", password=PASSWORD))

        assert tokens.refresh_token
        assert authenticate(f"Bearer {tokens.access_token}").id

    @pytest.mark.usefixtures("cognito")
    def test_unconfirmed_account(self) -> None:
        sign_up_handler(SignUpCommand(email="a@x.io", password=PASSWORD))

        with pytest.raises(AccountNotConfirmedError):
            sign_in_handler(SignInCommand(email="a@x.io", password=PASSWORD))

    @pytest.mark.usefixtures("cognito")
    def test_unknown_user_is_bad_credentials(self) -> None:
        with pytest.raises(InvalidCredentialsError):
            sign_in_handler(SignInCommand(email="nobody@x.io", password=PASSWORD))
