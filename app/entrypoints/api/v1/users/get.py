from uuid import UUID

from fastapi import APIRouter, Request

from app.domain.identity.query_service import UserQueryService
from app.domain.identity.schemas import UserResponse
from app.shared.auth.authorize import authorize_user

router = APIRouter(tags=["users"])

USER_QUERY_SERVICE = UserQueryService()


@router.get("/users/{user_sub}", description="Get a user by Cognito sub.")
def show_user(user_sub: UUID, request: Request) -> UserResponse:
    with authorize_user(request.headers):
        return USER_QUERY_SERVICE.get_user(user_sub)
