from typing import Any
from uuid import UUID

from app.domain.identity.exceptions import UserNotFoundError
from app.domain.identity.schemas import UserListResponse, UserResponse
from app.shared.clients.cognito import get_cognito


class UserQueryService:
    def get_user(self, sub: UUID) -> UserResponse:
        user = get_cognito().find_user_by_sub(str(sub))
        if user is None:
            raise UserNotFoundError
        return self._to_response(user)

    def list_users(self, limit: int, cursor: str | None = None) -> UserListResponse:
        users, next_cursor = get_cognito().list_users(limit, cursor)
        items = [self._to_response(item) for item in users]
        return UserListResponse(items=items, next_cursor=next_cursor)

    def user_exists(self, username: str) -> bool:
        return get_cognito().find_user_by_username(username) is not None

    def _to_response(self, user: dict[str, Any]) -> UserResponse:
        attributes = {a["Name"]: a["Value"] for a in user.get("Attributes", [])}
        return UserResponse(
            id=user["Username"],
            sub=attributes.get("sub"),
            status=user.get("UserStatus"),
            enabled=user.get("Enabled"),
        )
