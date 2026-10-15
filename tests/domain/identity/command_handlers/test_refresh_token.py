import pytest

from app.domain.identity.command_handlers.refresh_token import refresh_token_handler
from app.domain.identity.command_handlers.sign_in import sign_in_handler
from app.domain.identity.commands.refresh_token import RefreshTokenCommand
from app.domain.identity.commands.sign_in import SignInCommand
from app.domain.identity.exceptions import InvalidTokenError
from app.shared.auth.authorize import authenticate
from tests.fixtures.api import CognitoUsers

PASSWORD = "Passw0rd!x"


class TestRefreshTokenHandler:
    def test_issues_new_access_token(self, cognito_users: CognitoUsers) -> None:
        cognito_users.sign_in("a@x.io", PASSWORD)
        tokens = sign_in_handler(SignInCommand(email="a@x.io", password=PASSWORD))
        assert tokens.refresh_token

        refreshed = refresh_token_handler(RefreshTokenCommand(user_id="a@x.io", refresh_token=tokens.refresh_token))

        assert authenticate(f"Bearer {refreshed.access_token}").id == authenticate(f"Bearer {tokens.access_token}").id

    @pytest.mark.usefixtures("cognito")
    def test_invalid_refresh_token(self) -> None:
        with pytest.raises(InvalidTokenError):
            refresh_token_handler(RefreshTokenCommand(user_id="a@x.io", refresh_token="not-a-token"))
