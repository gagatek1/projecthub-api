from uuid import uuid4

from app.domain.project.commands.create_project import CreateProjectCommand
from app.domain.project.entity import ProjectEntity
from app.domain.project.repository import ProjectRepository
from app.domain.project.schemas import ProjectResponse


def create_project_handler(command: CreateProjectCommand) -> ProjectResponse:
    project = ProjectEntity(
        id=str(uuid4()),
        name=command.name,
        description=command.description,
        max_users=command.max_users,
        project_owner=command.owner_id,
    )
    ProjectRepository.create(project)
    return ProjectResponse.model_validate(project)
