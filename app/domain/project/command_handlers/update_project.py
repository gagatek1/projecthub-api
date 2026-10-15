from app.domain.project.commands.update_project import UpdateProjectCommand
from app.domain.project.repository import ProjectRepository
from app.domain.project.schemas import ProjectResponse


def update_project_handler(command: UpdateProjectCommand) -> ProjectResponse:
    project = ProjectRepository.update_as_owner(
        command.project_id,
        command.actor_id,
        name=command.name,
        description=command.description,
        max_users=command.max_users,
    )
    return ProjectResponse.model_validate(project)
