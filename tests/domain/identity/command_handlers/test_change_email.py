import pytest
from pydantic import SecretStr

from app.domain.identity.command_handlers.change_email import change_email_handler
from app.domain.identity.commands.change_email import ChangeEmailCommand
from app.domain.identity.exceptions import EmailTakenError, InvalidTokenError
from tests.fixtures.aws import CognitoFailure


class TestChangeEmailHandler:
    @pytest.mark.parametrize(
        ("code", "error"),
        [("AliasExistsException", EmailTakenError), ("NotAuthorizedException", InvalidTokenError)],
    )
    def test_maps_provider_errors(self, cognito_error: CognitoFailure, code: str, error: type[Exception]) -> None:
        cognito_error("update_email", code)

        with pytest.raises(error):
            change_email_handler(ChangeEmailCommand(access_token=SecretStr("token"), email="new@x.io"))
