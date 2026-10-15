import pytest

from app.domain.identity.command_handlers.confirm_forgot_password import confirm_forgot_password_handler
from app.domain.identity.commands.confirm_forgot_password import ConfirmForgotPasswordCommand
from app.domain.identity.exceptions import InvalidCodeError, InvalidPasswordError
from tests.fixtures.aws import CognitoFailure


class TestConfirmForgotPasswordHandler:
    @pytest.mark.parametrize(
        ("code", "error"),
        [
            ("CodeMismatchException", InvalidCodeError),
            ("ExpiredCodeException", InvalidCodeError),
            ("UserNotFoundException", InvalidCodeError),
            ("InvalidPasswordException", InvalidPasswordError),
        ],
    )
    def test_maps_provider_errors(self, cognito_error: CognitoFailure, code: str, error: type[Exception]) -> None:
        cognito_error("confirm_forgot_password", code)

        with pytest.raises(error):
            confirm_forgot_password_handler(
                ConfirmForgotPasswordCommand(email="a@x.io", confirmation_code="123456", new_password="N3wPassw0rd!")
            )
