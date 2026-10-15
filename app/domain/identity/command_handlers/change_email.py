from app.domain.identity.commands.change_email import ChangeEmailCommand
from app.domain.identity.exceptions import EmailTakenError, InvalidTokenError, translate
from app.shared.clients.cognito import CognitoError, get_cognito
from app.shared.errors import InvalidInputError

ERRORS = {
    "AliasExistsException": EmailTakenError,
    "NotAuthorizedException": InvalidTokenError,
    "InvalidParameterException": InvalidInputError,
}


def change_email_handler(command: ChangeEmailCommand) -> None:
    try:
        get_cognito().update_email(command.access_token.get_secret_value(), command.email)
    except CognitoError as exc:
        raise translate(exc, ERRORS) from exc
