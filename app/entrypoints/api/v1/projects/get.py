from typing import Annotated

from fastapi import APIRouter, Path, Request

from app.domain.project.query_service import ProjectQueryService
from app.domain.project.schemas import ProjectResponse
from app.shared.auth.authorize import authorize_user
from app.shared.types import ID_PATTERN

router = APIRouter(tags=["projects"])

PROJECT_QUERY_SERVICE = ProjectQueryService()


@router.get("/projects/{project_id}", description="Get one of the caller's projects.")
def show_project(
    project_id: Annotated[str, Path(pattern=ID_PATTERN, description="Project id")], request: Request
) -> ProjectResponse:
    with authorize_user(request.headers) as user:
        return PROJECT_QUERY_SERVICE.get_project(project_id, user.id)
