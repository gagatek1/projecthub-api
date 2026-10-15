from collections.abc import Generator, Mapping
from contextlib import contextmanager

from pydantic import BaseModel, ConfigDict, SecretStr

from app.shared.clients.cognito import CognitoError, get_cognito
from app.shared.errors import UnauthenticatedError

MAX_TOKEN_LENGTH = 8192
INVALID_TOKEN_CODES = frozenset({"NotAuthorizedException", "UserNotFoundException"})


class AuthUser(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    sub: str | None
    access_token: SecretStr


def authenticate(authorization: str | None) -> AuthUser:
    scheme, _, token = (authorization or "").partition(" ")
    token = token.strip()
    if scheme.lower() != "bearer" or not token or len(token) > MAX_TOKEN_LENGTH:
        raise UnauthenticatedError
    try:
        user = get_cognito().get_user(token)
    except CognitoError as exc:
        if exc.code in INVALID_TOKEN_CODES:
            raise UnauthenticatedError from exc
        raise
    attributes = {a["Name"]: a["Value"] for a in user.get("UserAttributes", [])}
    return AuthUser(id=user["Username"], sub=attributes.get("sub"), access_token=SecretStr(token))


@contextmanager
def authorize_user(headers: Mapping[str, str]) -> Generator[AuthUser]:
    yield authenticate(headers.get("authorization"))
