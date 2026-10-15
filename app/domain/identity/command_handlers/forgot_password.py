from app.domain.identity.commands.forgot_password import ForgotPasswordCommand
from app.domain.identity.exceptions import translate
from app.shared.clients.cognito import CognitoError, get_cognito

SILENT = frozenset({"UserNotFoundException", "InvalidParameterException"})


def forgot_password_handler(command: ForgotPasswordCommand) -> None:
    try:
        get_cognito().forgot_password(command.email)
    except CognitoError as exc:
        if exc.code in SILENT:
            return
        raise translate(exc, {}) from exc
