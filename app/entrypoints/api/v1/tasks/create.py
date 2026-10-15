from typing import Annotated

from fastapi import APIRouter, Path, Request, status

from app.domain.task.command_handlers.create_task import create_task_handler
from app.domain.task.commands.create_task import CreateTaskCommand
from app.domain.task.schemas import CreateTaskRequest, TaskResponse
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["tasks"])


@router.post(
    "/projects/{project_id}/tasks",
    status_code=status.HTTP_201_CREATED,
    description="Create a task in one of the caller's projects (assigned to the caller by default).",
)
def create_task(
    project_id: Annotated[str, Path(pattern=ID_PATTERN, description="Project id")],
    body: CreateTaskRequest,
    request: Request,
) -> TaskResponse:
    with authorize_user(request.headers) as user:
        return create_task_handler(CreateTaskCommand(project_id=project_id, actor_id=user.id, **body.model_dump()))
