from fastapi import APIRouter, Request, status

from app.domain.project.command_handlers.create_project import create_project_handler
from app.domain.project.commands.create_project import CreateProjectCommand
from app.domain.project.schemas import CreateProjectRequest, ProjectResponse
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["projects"])


@router.post("/projects", status_code=status.HTTP_201_CREATED, description="Create a project owned by the caller.")
def create_project(body: CreateProjectRequest, request: Request) -> ProjectResponse:
    with authorize_user(request.headers) as user:
        return create_project_handler(CreateProjectCommand(owner_id=user.id, **body.model_dump()))
