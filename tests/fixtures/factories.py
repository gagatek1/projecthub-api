from typing import Any
from uuid import uuid4

import factory

from app.domain.project.entity import ProjectEntity
from app.domain.task.entity import TaskEntity


class PynamoFactory[T: ProjectEntity | TaskEntity](factory.Factory[T]):
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class: type[T], *args: Any, **kwargs: Any) -> T:
        entity = model_class(*args, **kwargs)
        entity.save()
        return entity


class ProjectEntityFactory(PynamoFactory[ProjectEntity]):
    class Meta:
        model = ProjectEntity

    id = factory.LazyFunction(lambda: str(uuid4()))
    name = factory.Sequence(lambda n: f"Project {n}")
    description = "Moon"
    max_users = 3
    project_owner = "alice"


class TaskEntityFactory(PynamoFactory[TaskEntity]):
    class Meta:
        model = TaskEntity

    id = factory.LazyFunction(lambda: str(uuid4()))
    project_id = factory.LazyFunction(lambda: ProjectEntityFactory.create().id)
    name = factory.Sequence(lambda n: f"Task {n}")
    description = "d"
    assigned_user = "alice"
