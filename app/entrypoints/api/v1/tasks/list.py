from typing import Annotated

from fastapi import APIRouter, Path, Query, Request

from app.domain.task.query_service import TaskQueryService
from app.domain.task.schemas import TaskListResponse
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["tasks"])

TASK_QUERY_SERVICE = TaskQueryService()


@router.get(
    "/projects/{project_id}/tasks",
    description="List tasks of a project: all for the owner, only own assigned tasks for others.",
)
def show_tasks(
    project_id: Annotated[str, Path(pattern=ID_PATTERN, description="Project id")],
    request: Request,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    cursor: Annotated[str | None, Query(max_length=2048)] = None,
) -> TaskListResponse:
    with authorize_user(request.headers) as user:
        return TASK_QUERY_SERVICE.list_tasks(project_id, user.id, limit, cursor)
