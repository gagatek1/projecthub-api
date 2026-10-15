from pynamodb.expressions.condition import Condition

from app.domain.project.exceptions import ProjectForbiddenError
from app.domain.project.query_service import ProjectQueryService
from app.domain.task.entity import TaskEntity
from app.domain.task.exceptions import TaskNotFoundError
from app.domain.task.schemas import TaskListResponse, TaskResponse, TaskSummaryResponse
from app.shared.pagination import decode_cursor, encode_cursor


class TaskQueryService:
    def get_task(self, project_id: str, task_id: str, actor_id: str) -> TaskResponse:
        pk = f"project#{project_id}"
        sk = f"task#{task_id}"
        try:
            task = TaskEntity.get(pk, sk)
        except TaskEntity.DoesNotExist as exc:
            raise TaskNotFoundError from exc
        if task.assigned_user != actor_id:
            ProjectQueryService().get_project(project_id, actor_id)
        return TaskResponse.model_validate(task)

    def list_tasks(self, project_id: str, actor_id: str, limit: int, cursor: str | None = None) -> TaskListResponse:
        pk = f"project#{project_id}"
        visible_to_actor: Condition | None = None
        try:
            ProjectQueryService().get_project(project_id, actor_id)
        except ProjectForbiddenError:
            visible_to_actor = TaskEntity.assigned_user == actor_id
        tasks = TaskEntity.query(
            pk,
            TaskEntity.sk.startswith("task#"),
            filter_condition=visible_to_actor,
            limit=limit,
            last_evaluated_key=decode_cursor(cursor, pk=pk),
        )
        items = [TaskSummaryResponse.model_validate(item) for item in tasks]
        return TaskListResponse(items=items, next_cursor=encode_cursor(tasks.last_evaluated_key))

    def has_tasks(self, project_id: str) -> bool:
        pk = f"project#{project_id}"
        return TaskEntity.count(pk, TaskEntity.sk.startswith("task#"), limit=1) > 0
