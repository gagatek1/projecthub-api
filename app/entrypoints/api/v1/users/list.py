from typing import Annotated

from fastapi import APIRouter, Query, Request

from app.domain.identity.query_service import UserQueryService
from app.domain.identity.schemas import UserListResponse
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["users"])

USER_QUERY_SERVICE = UserQueryService()


@router.get("/users", description="List users (id, sub, status), paginated with next_cursor.")
def show_users(
    request: Request,
    limit: Annotated[int, Query(ge=1, le=60)] = 20,
    cursor: Annotated[str | None, Query(max_length=2048)] = None,
) -> UserListResponse:
    with authorize_user(request.headers):
        return USER_QUERY_SERVICE.list_users(limit, cursor)
