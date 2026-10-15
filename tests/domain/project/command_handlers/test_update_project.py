import pytest

from app.domain.project.command_handlers.update_project import update_project_handler
from app.domain.project.commands.update_project import UpdateProjectCommand
from app.domain.project.exceptions import ProjectForbiddenError, ProjectNotFoundError
from app.domain.project.query_service import ProjectQueryService
from app.domain.project.schemas import ProjectResponse
from tests.fixtures.factories import ProjectEntityFactory


def _update(project_id: str, actor: str) -> ProjectResponse:
    return update_project_handler(
        UpdateProjectCommand(project_id=project_id, actor_id=actor, name="Artemis", description="d", max_users=5)
    )


@pytest.mark.usefixtures("dynamodb")
class TestUpdateProjectHandler:
    def test_owner_changes_fields(self) -> None:
        project = ProjectEntityFactory.create()

        updated = _update(project.id, "alice")

        assert (updated.name, updated.max_users) == ("Artemis", 5)
        assert ProjectQueryService().get_project(project.id, "alice") == updated

    def test_other_user_is_forbidden_and_item_is_unchanged(self) -> None:
        project = ProjectEntityFactory.create()

        with pytest.raises(ProjectForbiddenError):
            _update(project.id, "mallory")

        assert ProjectQueryService().get_project(project.id, "alice") == ProjectResponse.model_validate(project)

    def test_missing_project_raises_not_found_and_does_not_upsert(self) -> None:
        with pytest.raises(ProjectNotFoundError):
            _update("missing", "alice")
        with pytest.raises(ProjectNotFoundError):
            ProjectQueryService().get_project("missing", "alice")
