from app.domain.identity.commands.change_password import ChangePasswordCommand
from app.domain.identity.exceptions import InvalidCredentialsError, translate
from app.shared.clients.cognito import CognitoError, get_cognito

ERRORS = {"NotAuthorizedException": InvalidCredentialsError}


def change_password_handler(command: ChangePasswordCommand) -> None:
    try:
        get_cognito().change_password(
            command.access_token.get_secret_value(), command.old_password, command.new_password
        )
    except CognitoError as exc:
        raise translate(exc, ERRORS) from exc
