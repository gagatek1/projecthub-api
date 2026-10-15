from app.shared.errors import ConflictError, NotFoundError, PermissionDeniedError


class ProjectNotFoundError(NotFoundError):
    default_message = "Project not found"


class ProjectForbiddenError(PermissionDeniedError):
    default_message = "Only the project owner can access this project"


class ProjectHasTasksError(ConflictError):
    default_message = "Delete the project's tasks first"
