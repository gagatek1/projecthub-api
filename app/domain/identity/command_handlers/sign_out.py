from app.domain.identity.commands.sign_out import SignOutCommand
from app.domain.identity.exceptions import InvalidTokenError, translate
from app.shared.clients.cognito import CognitoError, get_cognito

ERRORS = {"NotAuthorizedException": InvalidTokenError}


def sign_out_handler(command: SignOutCommand) -> None:
    try:
        get_cognito().global_sign_out(command.access_token.get_secret_value())
    except CognitoError as exc:
        raise translate(exc, ERRORS) from exc
