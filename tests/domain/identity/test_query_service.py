from uuid import UUID, uuid4

import pytest

from app.domain.identity.command_handlers.sign_up import sign_up_handler
from app.domain.identity.commands.sign_up import SignUpCommand
from app.domain.identity.exceptions import UserNotFoundError
from app.domain.identity.query_service import UserQueryService

PASSWORD = "Passw0rd!x"


@pytest.mark.usefixtures("cognito")
class TestUserQueryService:
    def test_get_user_by_sub(self) -> None:
        sub = sign_up_handler(SignUpCommand(email="a@x.io", password=PASSWORD)).sub

        user = UserQueryService().get_user(UUID(sub))

        assert user.sub == sub
        assert "email" not in user.model_dump()

    def test_get_unknown_user(self) -> None:
        with pytest.raises(UserNotFoundError):
            UserQueryService().get_user(uuid4())

    def test_list_users_paginated(self) -> None:
        subs = {sign_up_handler(SignUpCommand(email=f"u{i}@x.io", password=PASSWORD)).sub for i in range(3)}

        first = UserQueryService().list_users(limit=2)
        second = UserQueryService().list_users(limit=2, cursor=first.next_cursor)

        assert len(first.items) == 2
        assert {u.sub for u in first.items + second.items} == subs

    def test_user_exists(self) -> None:
        sign_up_handler(SignUpCommand(email="a@x.io", password=PASSWORD))
        username = UserQueryService().list_users(limit=1).items[0].id

        assert UserQueryService().user_exists(username) is True
        assert UserQueryService().user_exists("ghost") is False
