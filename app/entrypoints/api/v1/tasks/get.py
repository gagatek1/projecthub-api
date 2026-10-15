from typing import Annotated

from fastapi import APIRouter, Path, Request

from app.domain.task.query_service import TaskQueryService
from app.domain.task.schemas import TaskResponse
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["tasks"])

TASK_QUERY_SERVICE = TaskQueryService()


@router.get("/projects/{project_id}/tasks/{task_id}", description="Get a task (project owner or assigned user).")
def show_task(
    project_id: Annotated[str, Path(pattern=ID_PATTERN, description="Project id")],
    task_id: Annotated[str, Path(pattern=ID_PATTERN, description="Task id")],
    request: Request,
) -> TaskResponse:
    with authorize_user(request.headers) as user:
        return TASK_QUERY_SERVICE.get_task(project_id, task_id, user.id)
