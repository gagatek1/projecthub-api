from app.domain.identity.query_service import UserQueryService
from app.domain.task.commands.create_task import CreateTaskCommand
from app.domain.task.entity import TaskEntity
from app.domain.task.exceptions import TaskAssigneeNotFoundError
from app.domain.task.repository import TaskRepository
from app.domain.task.schemas import TaskResponse


def create_task_handler(command: CreateTaskCommand) -> TaskResponse:
    assignee = command.assigned_user or command.actor_id
    if assignee != command.actor_id and not UserQueryService().user_exists(assignee):
        raise TaskAssigneeNotFoundError
    task = TaskEntity(
        project_id=command.project_id,
        name=command.name,
        description=command.description,
        assigned_user=assignee,
    )
    TaskRepository.create_in_project(task, command.actor_id)
    return TaskResponse.model_validate(task)
