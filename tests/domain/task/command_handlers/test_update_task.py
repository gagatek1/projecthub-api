import pytest

from app.domain.task.command_handlers.update_task import update_task_handler
from app.domain.task.commands.update_task import UpdateTaskCommand
from app.domain.task.exceptions import TaskAssigneeNotFoundError, TaskForbiddenError, TaskNotFoundError
from app.domain.task.query_service import TaskQueryService
from app.domain.task.schemas import TaskResponse
from tests.fixtures.factories import ProjectEntityFactory, TaskEntityFactory


def _update(
    project_id: str, task_id: str, actor: str = "alice", name: str = "T", assigned_user: str | None = None
) -> TaskResponse:
    return update_task_handler(
        UpdateTaskCommand(
            project_id=project_id,
            task_id=task_id,
            actor_id=actor,
            name=name,
            description="d",
            assigned_user=assigned_user,
        )
    )


@pytest.mark.usefixtures("dynamodb", "known_users")
class TestUpdateTaskHandler:
    def test_keeps_assignee_when_omitted(self) -> None:
        task = TaskEntityFactory.create()

        updated = _update(task.project_id, task.id, name="T2")

        assert (updated.name, updated.assigned_user) == ("T2", "alice")
        assert TaskQueryService().get_task(task.project_id, task.id, "alice") == updated

    def test_reassigns_to_existing_user_only(self) -> None:
        task = TaskEntityFactory.create()

        with pytest.raises(TaskAssigneeNotFoundError):
            _update(task.project_id, task.id, assigned_user="ghost")
        assert _update(task.project_id, task.id, assigned_user="bob").assigned_user == "bob"

    def test_owner_who_is_not_assignee_is_forbidden(self) -> None:
        task = TaskEntityFactory.create(assigned_user="bob")

        with pytest.raises(TaskForbiddenError):
            _update(task.project_id, task.id, name="X")

    def test_missing_task_raises_not_found_and_does_not_upsert(self) -> None:
        project = ProjectEntityFactory.create()

        with pytest.raises(TaskNotFoundError):
            _update(project.id, "missing")
        with pytest.raises(TaskNotFoundError):
            TaskQueryService().get_task(project.id, "missing", "alice")
