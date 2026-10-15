from typing import Annotated

from fastapi import APIRouter, Path, Request, Response, status

from app.domain.task.command_handlers.delete_task import delete_task_handler
from app.domain.task.commands.delete_task import DeleteTaskCommand
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["tasks"])


@router.delete(
    "/projects/{project_id}/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    description="Delete a task (assigned user only).",
)
def delete_task(
    project_id: Annotated[str, Path(pattern=ID_PATTERN, description="Project id")],
    task_id: Annotated[str, Path(pattern=ID_PATTERN, description="Task id")],
    request: Request,
) -> None:
    with authorize_user(request.headers) as user:
        delete_task_handler(DeleteTaskCommand(project_id=project_id, task_id=task_id, actor_id=user.id))
