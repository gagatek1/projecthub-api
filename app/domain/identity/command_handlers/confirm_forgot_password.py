from app.domain.identity.commands.confirm_forgot_password import ConfirmForgotPasswordCommand
from app.domain.identity.exceptions import InvalidCodeError, translate
from app.shared.clients.cognito import CognitoError, get_cognito

ERRORS = {
    "CodeMismatchException": InvalidCodeError,
    "ExpiredCodeException": InvalidCodeError,
    "UserNotFoundException": InvalidCodeError,
}


def confirm_forgot_password_handler(command: ConfirmForgotPasswordCommand) -> None:
    try:
        get_cognito().confirm_forgot_password(command.email, command.confirmation_code, command.new_password)
    except CognitoError as exc:
        raise translate(exc, ERRORS) from exc
