from app.domain.identity.query_service import UserQueryService
from app.domain.task.commands.update_task import UpdateTaskCommand
from app.domain.task.exceptions import TaskAssigneeNotFoundError
from app.domain.task.repository import TaskRepository
from app.domain.task.schemas import TaskResponse


def update_task_handler(command: UpdateTaskCommand) -> TaskResponse:
    assignee = command.assigned_user or command.actor_id
    if assignee != command.actor_id and not UserQueryService().user_exists(assignee):
        raise TaskAssigneeNotFoundError
    task = TaskRepository.update_as_assignee(
        command.project_id,
        command.task_id,
        command.actor_id,
        name=command.name,
        description=command.description,
        assigned_user=assignee,
    )
    return TaskResponse.model_validate(task)
