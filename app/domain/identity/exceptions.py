from collections.abc import Mapping

from app.shared.clients.cognito import CognitoError
from app.shared.errors import (
    AlreadyExistsError,
    DomainError,
    InvalidInputError,
    NotFoundError,
    PermissionDeniedError,
    RateLimitedError,
    UnauthenticatedError,
)


class UserNotFoundError(NotFoundError):
    default_message = "User not found"


class EmailTakenError(AlreadyExistsError):
    default_message = "An account with the given email already exists"


class AccountNotConfirmedError(PermissionDeniedError):
    default_message = "Please verify your account"


class InvalidCredentialsError(UnauthenticatedError):
    default_message = "Incorrect username or password"


class InvalidTokenError(UnauthenticatedError):
    default_message = "Invalid or expired token"


class InvalidCodeError(InvalidInputError):
    default_message = "The provided code is invalid or expired"


class InvalidPasswordError(InvalidInputError):
    default_message = "Password does not meet the policy"


class TooManyAttemptsError(RateLimitedError):
    pass


COMMON_ERRORS: Mapping[str, type[DomainError]] = {
    "LimitExceededException": TooManyAttemptsError,
    "TooManyRequestsException": TooManyAttemptsError,
    "TooManyFailedAttemptsException": TooManyAttemptsError,
    "InvalidPasswordException": InvalidPasswordError,
}


def translate(error: CognitoError, mapping: Mapping[str, type[DomainError]]) -> DomainError:
    error_type = mapping.get(error.code) or COMMON_ERRORS.get(error.code)
    return error_type() if error_type else error
