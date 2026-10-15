from typing import Annotated

from fastapi import APIRouter, Path, Request

from app.domain.project.command_handlers.update_project import update_project_handler
from app.domain.project.commands.update_project import UpdateProjectCommand
from app.domain.project.schemas import ProjectResponse, UpdateProjectRequest
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["projects"])


@router.put("/projects/{project_id}", description="Update a project (owner only).")
def update_project(
    project_id: Annotated[str, Path(pattern=ID_PATTERN, description="Project id")],
    body: UpdateProjectRequest,
    request: Request,
) -> ProjectResponse:
    with authorize_user(request.headers) as user:
        return update_project_handler(
            UpdateProjectCommand(project_id=project_id, actor_id=user.id, **body.model_dump())
        )
