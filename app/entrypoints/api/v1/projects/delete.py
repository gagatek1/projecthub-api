from typing import Annotated

from fastapi import APIRouter, Path, Request, Response, status

from app.domain.project.command_handlers.delete_project import delete_project_handler
from app.domain.project.commands.delete_project import DeleteProjectCommand
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["projects"])


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    description="Delete a project (owner only).",
)
def delete_project(
    project_id: Annotated[str, Path(pattern=ID_PATTERN, description="Project id")], request: Request
) -> None:
    with authorize_user(request.headers) as user:
        delete_project_handler(DeleteProjectCommand(project_id=project_id, actor_id=user.id))
