import pytest

from app.domain.project.exceptions import ProjectForbiddenError
from app.domain.task.command_handlers.delete_task import delete_task_handler
from app.domain.task.commands.delete_task import DeleteTaskCommand
from app.domain.task.exceptions import TaskNotFoundError
from tests.fixtures.factories import TaskEntityFactory


def _delete(project_id: str, task_id: str, actor: str) -> None:
    delete_task_handler(DeleteTaskCommand(project_id=project_id, task_id=task_id, actor_id=actor))


@pytest.mark.usefixtures("dynamodb")
class TestDeleteTaskHandler:
    def test_assignee_deletes(self) -> None:
        task = TaskEntityFactory.create()

        _delete(task.project_id, task.id, "alice")

        with pytest.raises(TaskNotFoundError):
            _delete(task.project_id, task.id, "alice")

    def test_outsider_is_forbidden(self) -> None:
        task = TaskEntityFactory.create()

        with pytest.raises(ProjectForbiddenError):
            _delete(task.project_id, task.id, "bob")
