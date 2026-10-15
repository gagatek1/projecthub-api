from typing import NoReturn

from pynamodb.exceptions import DeleteError, TransactWriteError, UpdateError
from pynamodb.expressions.condition import Condition

from app.domain.project.entity import ProjectEntity
from app.domain.project.query_service import ProjectQueryService
from app.domain.task.entity import TaskEntity
from app.domain.task.exceptions import TaskForbiddenError
from app.domain.task.query_service import TaskQueryService
from app.shared.entities.base import transaction


class TaskRepository:
    @staticmethod
    def create_in_project(task: TaskEntity, owner_id: str) -> None:
        try:
            with transaction() as tx:
                tx.condition_check(
                    ProjectEntity,
                    "project",
                    f"project#{task.project_id}",
                    condition=ProjectEntity.project_owner == owner_id,
                )
                tx.save(task, condition=TaskEntity.pk.does_not_exist())
        except TransactWriteError:
            ProjectQueryService().get_project(task.project_id, owner_id)
            raise

    @classmethod
    def update_as_assignee(
        cls,
        project_id: str,
        task_id: str,
        actor: str,
        *,
        name: str,
        description: str,
        assigned_user: str,
    ) -> TaskEntity:
        task = TaskEntity(id=task_id, project_id=project_id, name=name, description=description, assigned_user=actor)
        try:
            task.update(
                actions=[
                    TaskEntity.name.set(name),
                    TaskEntity.description.set(description),
                    TaskEntity.assigned_user.set(assigned_user),
                ],
                condition=cls._assigned_to(actor),
            )
        except UpdateError as exc:
            cls._raise_for_failed_condition(project_id, task_id, actor, exc)
        return task

    @classmethod
    def delete_as_assignee(cls, project_id: str, task_id: str, actor: str) -> None:
        task = TaskEntity(id=task_id, project_id=project_id, name="", description="", assigned_user=actor)
        try:
            task.delete(condition=cls._assigned_to(actor))
        except DeleteError as exc:
            cls._raise_for_failed_condition(project_id, task_id, actor, exc)

    @staticmethod
    def _assigned_to(actor: str) -> Condition:
        return TaskEntity.pk.exists() & (TaskEntity.assigned_user == actor)

    @staticmethod
    def _raise_for_failed_condition(
        project_id: str, task_id: str, actor: str, exc: UpdateError | DeleteError
    ) -> NoReturn:
        if exc.cause_response_code != "ConditionalCheckFailedException":
            raise exc
        TaskQueryService().get_task(project_id, task_id, actor)
        raise TaskForbiddenError from exc
