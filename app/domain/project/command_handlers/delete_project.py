from app.domain.project.commands.delete_project import DeleteProjectCommand
from app.domain.project.exceptions import ProjectHasTasksError
from app.domain.project.query_service import ProjectQueryService
from app.domain.project.repository import ProjectRepository
from app.domain.task.query_service import TaskQueryService


def delete_project_handler(command: DeleteProjectCommand) -> None:
    ProjectQueryService().get_project(command.project_id, command.actor_id)
    if TaskQueryService().has_tasks(command.project_id):
        raise ProjectHasTasksError
    ProjectRepository.delete_as_owner(command.project_id, command.actor_id)
