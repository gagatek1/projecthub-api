from typing import Annotated

from fastapi import APIRouter, Query, Request

from app.domain.project.query_service import ProjectQueryService
from app.domain.project.schemas import ProjectListResponse
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["projects"])

PROJECT_QUERY_SERVICE = ProjectQueryService()


@router.get("/projects", description="List the caller's projects, paginated with next_cursor.")
def show_projects(
    request: Request,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    cursor: Annotated[str | None, Query(max_length=2048)] = None,
) -> ProjectListResponse:
    with authorize_user(request.headers) as user:
        return PROJECT_QUERY_SERVICE.list_projects(user.id, limit, cursor)
