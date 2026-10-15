from app.shared.errors import NotFoundError, PermissionDeniedError


class TaskNotFoundError(NotFoundError):
    default_message = "Task not found"


class TaskForbiddenError(PermissionDeniedError):
    default_message = "Only the assigned user can change this task"


class TaskAssigneeNotFoundError(NotFoundError):
    default_message = "Assigned user not found"
