import pytest

from app.domain.project.exceptions import ProjectForbiddenError, ProjectNotFoundError
from app.domain.project.query_service import ProjectQueryService
from app.domain.project.schemas import ProjectResponse
from app.shared.pagination import InvalidCursorError, encode_cursor
from tests.fixtures.factories import ProjectEntityFactory


@pytest.mark.usefixtures("dynamodb")
class TestProjectQueryService:
    def test_get_returns_project_to_owner(self) -> None:
        project = ProjectEntityFactory.create()

        assert ProjectQueryService().get_project(project.id, "alice") == ProjectResponse.model_validate(project)

    def test_get_by_other_user_is_forbidden(self) -> None:
        project = ProjectEntityFactory.create()

        with pytest.raises(ProjectForbiddenError):
            ProjectQueryService().get_project(project.id, "mallory")

    def test_get_missing_raises_not_found(self) -> None:
        with pytest.raises(ProjectNotFoundError):
            ProjectQueryService().get_project("missing", "alice")

    def test_list_returns_only_own_projects_paginated(self) -> None:
        mine = {p.id for p in ProjectEntityFactory.create_batch(3)}
        ProjectEntityFactory.create(project_owner="bob")

        first = ProjectQueryService().list_projects("alice", limit=2)
        second = ProjectQueryService().list_projects("alice", limit=2, cursor=first.next_cursor)

        assert len(first.items) == 2
        assert first.next_cursor is not None
        assert {p.id for p in first.items + second.items} == mine

    @pytest.mark.parametrize(
        "cursor",
        [
            "not-base64!",
            encode_cursor({"pk": {"S": "project#other"}, "sk": {"S": "task#1"}}),
            encode_cursor({"pk": {"S": "project"}, "sk": {"S": "x"}, "extra": {"S": "y"}}),
        ],
    )
    def test_list_rejects_tampered_cursor(self, cursor: str) -> None:
        with pytest.raises(InvalidCursorError):
            ProjectQueryService().list_projects("alice", limit=2, cursor=cursor)
