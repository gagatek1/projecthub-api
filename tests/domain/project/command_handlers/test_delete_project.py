import pytest

from app.domain.project.command_handlers.delete_project import delete_project_handler
from app.domain.project.commands.delete_project import DeleteProjectCommand
from app.domain.project.exceptions import ProjectForbiddenError, ProjectHasTasksError, ProjectNotFoundError
from app.domain.project.query_service import ProjectQueryService
from tests.fixtures.factories import ProjectEntityFactory, TaskEntityFactory


def _delete(project_id: str, actor: str) -> None:
    delete_project_handler(DeleteProjectCommand(project_id=project_id, actor_id=actor))


@pytest.mark.usefixtures("dynamodb")
class TestDeleteProjectHandler:
    def test_owner_deletes(self) -> None:
        project = ProjectEntityFactory.create()

        _delete(project.id, "alice")

        with pytest.raises(ProjectNotFoundError):
            ProjectQueryService().get_project(project.id, "alice")

    def test_other_user_is_forbidden(self) -> None:
        project = ProjectEntityFactory.create()

        with pytest.raises(ProjectForbiddenError):
            _delete(project.id, "mallory")

        assert ProjectQueryService().get_project(project.id, "alice").id == project.id

    def test_missing_project_raises_not_found(self) -> None:
        with pytest.raises(ProjectNotFoundError):
            _delete("missing", "alice")

    def test_project_with_tasks_is_refused(self) -> None:
        project = ProjectEntityFactory.create()
        TaskEntityFactory.create(project_id=project.id)

        with pytest.raises(ProjectHasTasksError):
            _delete(project.id, "alice")

        assert ProjectQueryService().get_project(project.id, "alice").id == project.id
