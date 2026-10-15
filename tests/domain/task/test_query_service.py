import pytest

from app.domain.project.exceptions import ProjectForbiddenError
from app.domain.task.exceptions import TaskNotFoundError
from app.domain.task.query_service import TaskQueryService
from app.domain.task.schemas import TaskResponse
from tests.fixtures.factories import ProjectEntityFactory, TaskEntityFactory


@pytest.mark.usefixtures("dynamodb")
class TestTaskQueryService:
    def test_owner_lists_all_tasks_assignee_only_own(self) -> None:
        project = ProjectEntityFactory.create()
        own = TaskEntityFactory.create(project_id=project.id)
        bobs = TaskEntityFactory.create(project_id=project.id, assigned_user="bob")

        assert {t.id for t in TaskQueryService().list_tasks(project.id, "alice", limit=10).items} == {own.id, bobs.id}
        assert [t.id for t in TaskQueryService().list_tasks(project.id, "bob", limit=10).items] == [bobs.id]

    def test_list_is_paginated(self) -> None:
        project = ProjectEntityFactory.create()
        created = {t.id for t in TaskEntityFactory.create_batch(3, project_id=project.id)}

        first = TaskQueryService().list_tasks(project.id, "alice", limit=2)
        second = TaskQueryService().list_tasks(project.id, "alice", limit=2, cursor=first.next_cursor)

        assert {t.id for t in first.items + second.items} == created

    def test_get_by_assignee(self) -> None:
        task = TaskEntityFactory.create(assigned_user="bob")

        assert TaskQueryService().get_task(task.project_id, task.id, "bob") == TaskResponse.model_validate(task)

    def test_get_by_outsider_is_forbidden(self) -> None:
        task = TaskEntityFactory.create()

        with pytest.raises(ProjectForbiddenError):
            TaskQueryService().get_task(task.project_id, task.id, "bob")

    def test_get_missing_raises_not_found(self) -> None:
        project = ProjectEntityFactory.create()

        with pytest.raises(TaskNotFoundError):
            TaskQueryService().get_task(project.id, "missing", "alice")

    def test_has_tasks(self) -> None:
        project = ProjectEntityFactory.create()

        assert TaskQueryService().has_tasks(project.id) is False
        TaskEntityFactory.create(project_id=project.id)
        assert TaskQueryService().has_tasks(project.id) is True
