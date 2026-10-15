from app.domain.identity.commands.verify_account import VerifyAccountCommand
from app.domain.identity.exceptions import InvalidCodeError, translate
from app.shared.clients.cognito import CognitoError, get_cognito

ERRORS = {
    "CodeMismatchException": InvalidCodeError,
    "ExpiredCodeException": InvalidCodeError,
    "UserNotFoundException": InvalidCodeError,
}


def verify_account_handler(command: VerifyAccountCommand) -> None:
    try:
        get_cognito().confirm_sign_up(command.email, command.confirmation_code)
    except CognitoError as exc:
        raise translate(exc, ERRORS) from exc
