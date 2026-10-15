from app.domain.identity.commands.refresh_token import RefreshTokenCommand
from app.domain.identity.exceptions import InvalidTokenError, translate
from app.domain.identity.schemas import TokenResponse
from app.shared.clients.cognito import CognitoError, get_cognito

ERRORS = {"NotAuthorizedException": InvalidTokenError, "InvalidParameterException": InvalidTokenError}


def refresh_token_handler(command: RefreshTokenCommand) -> TokenResponse:
    try:
        result = get_cognito().initiate_auth(
            "REFRESH_TOKEN_AUTH", command.user_id, {"REFRESH_TOKEN": command.refresh_token}
        )
    except CognitoError as exc:
        raise translate(exc, ERRORS) from exc
    if "AccessToken" not in result:
        raise InvalidTokenError
    return TokenResponse(access_token=result["AccessToken"], expires_in=result["ExpiresIn"])
