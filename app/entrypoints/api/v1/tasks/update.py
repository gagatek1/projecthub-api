from typing import Annotated

from fastapi import APIRouter, Path, Request

from app.domain.task.command_handlers.update_task import update_task_handler
from app.domain.task.commands.update_task import UpdateTaskCommand
from app.domain.task.schemas import TaskResponse, UpdateTaskRequest
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["tasks"])


@router.put("/projects/{project_id}/tasks/{task_id}", description="Update a task (assigned user only).")
def update_task(
    project_id: Annotated[str, Path(pattern=ID_PATTERN, description="Project id")],
    task_id: Annotated[str, Path(pattern=ID_PATTERN, description="Task id")],
    body: UpdateTaskRequest,
    request: Request,
) -> TaskResponse:
    with authorize_user(request.headers) as user:
        return update_task_handler(
            UpdateTaskCommand(project_id=project_id, task_id=task_id, actor_id=user.id, **body.model_dump())
        )
