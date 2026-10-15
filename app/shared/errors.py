class DomainError(Exception):
    default_message = "Domain error"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.default_message
        super().__init__(self.message)


class NotFoundError(DomainError):
    default_message = "Resource not found"


class AlreadyExistsError(DomainError):
    default_message = "Resource already exists"


class BusinessRuleError(DomainError):
    default_message = "Operation not allowed in current state"


class PermissionDeniedError(DomainError):
    default_message = "Permission denied"


class ExternalServiceError(DomainError):
    default_message = "External service failure"


class UnauthenticatedError(DomainError):
    default_message = "Not authenticated"


class InvalidInputError(DomainError):
    default_message = "Invalid input"


class RateLimitedError(DomainError):
    default_message = "Too many attempts, please try again later"


class ConflictError(DomainError):
    default_message = "Operation conflicts with the current state"
