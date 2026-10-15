import pytest

from app.domain.project.exceptions import ProjectForbiddenError, ProjectNotFoundError
from app.domain.task.command_handlers.create_task import create_task_handler
from app.domain.task.commands.create_task import CreateTaskCommand
from app.domain.task.exceptions import TaskAssigneeNotFoundError
from app.domain.task.query_service import TaskQueryService
from app.domain.task.schemas import TaskResponse
from tests.fixtures.factories import ProjectEntityFactory


def _create(project_id: str, actor: str = "alice", assigned_user: str | None = None) -> TaskResponse:
    return create_task_handler(
        CreateTaskCommand(project_id=project_id, actor_id=actor, name="T", description="d", assigned_user=assigned_user)
    )


@pytest.mark.usefixtures("dynamodb", "known_users")
class TestCreateTaskHandler:
    def test_assigns_creator_by_default(self) -> None:
        project = ProjectEntityFactory.create()

        task = _create(project.id)

        assert (task.assigned_user, task.project_id) == ("alice", project.id)
        assert TaskQueryService().get_task(project.id, task.id, "alice") == task

    def test_assigns_existing_user(self) -> None:
        assert _create(ProjectEntityFactory.create().id, assigned_user="bob").assigned_user == "bob"

    def test_unknown_assignee_is_rejected(self) -> None:
        project = ProjectEntityFactory.create()

        with pytest.raises(TaskAssigneeNotFoundError):
            _create(project.id, assigned_user="ghost")

        assert TaskQueryService().list_tasks(project.id, "alice", limit=10).items == []

    def test_unknown_project_is_rejected(self) -> None:
        with pytest.raises(ProjectNotFoundError):
            _create("nope")

    def test_someone_elses_project_is_forbidden(self) -> None:
        with pytest.raises(ProjectForbiddenError):
            _create(ProjectEntityFactory.create().id, actor="bob")
