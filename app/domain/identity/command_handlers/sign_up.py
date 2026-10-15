from app.domain.identity.commands.sign_up import SignUpCommand
from app.domain.identity.exceptions import EmailTakenError, translate
from app.domain.identity.schemas import SignUpResponse
from app.shared.clients.cognito import CognitoError, get_cognito
from app.shared.errors import InvalidInputError

ERRORS = {"UsernameExistsException": EmailTakenError, "InvalidParameterException": InvalidInputError}


def sign_up_handler(command: SignUpCommand) -> SignUpResponse:
    try:
        response = get_cognito().sign_up(command.email, command.password)
    except CognitoError as exc:
        raise translate(exc, ERRORS) from exc
    return SignUpResponse(sub=response["UserSub"])
