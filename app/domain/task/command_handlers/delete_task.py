from app.domain.task.commands.delete_task import DeleteTaskCommand
from app.domain.task.repository import TaskRepository


def delete_task_handler(command: DeleteTaskCommand) -> None:
    TaskRepository.delete_as_assignee(command.project_id, command.task_id, command.actor_id)
