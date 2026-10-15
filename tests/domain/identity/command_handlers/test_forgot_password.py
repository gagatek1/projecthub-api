import pytest

from app.domain.identity.command_handlers.forgot_password import forgot_password_handler
from app.domain.identity.commands.forgot_password import ForgotPasswordCommand
from app.shared.errors import ExternalServiceError
from tests.fixtures.aws import CognitoFailure


class TestForgotPasswordHandler:
    @pytest.mark.parametrize("code", ["UserNotFoundException", "InvalidParameterException"])
    def test_does_not_reveal_whether_the_account_exists(self, cognito_error: CognitoFailure, code: str) -> None:
        cognito_error("forgot_password", code)

        forgot_password_handler(ForgotPasswordCommand(email="a@x.io"))

    def test_provider_failure(self, cognito_error: CognitoFailure) -> None:
        cognito_error("forgot_password", "InternalErrorException")

        with pytest.raises(ExternalServiceError):
            forgot_password_handler(ForgotPasswordCommand(email="a@x.io"))
