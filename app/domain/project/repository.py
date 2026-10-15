from typing import NoReturn

from pynamodb.exceptions import DeleteError, UpdateError
from pynamodb.expressions.condition import Condition

from app.domain.project.entity import ProjectEntity
from app.domain.project.exceptions import ProjectForbiddenError
from app.domain.project.query_service import ProjectQueryService


class ProjectRepository:
    @staticmethod
    def create(project: ProjectEntity) -> None:
        project.save(condition=ProjectEntity.pk.does_not_exist())

    @classmethod
    def update_as_owner(
        cls, project_id: str, owner: str, *, name: str, description: str, max_users: int
    ) -> ProjectEntity:
        project = ProjectEntity(
            id=project_id, name=name, description=description, max_users=max_users, project_owner=owner
        )
        try:
            project.update(
                actions=[
                    ProjectEntity.name.set(name),
                    ProjectEntity.description.set(description),
                    ProjectEntity.max_users.set(max_users),
                ],
                condition=cls._owned_by(owner),
            )
        except UpdateError as exc:
            cls._raise_for_failed_condition(project_id, owner, exc)
        return project

    @classmethod
    def delete_as_owner(cls, project_id: str, owner: str) -> None:
        project = ProjectEntity(id=project_id, name="", description="", max_users=1, project_owner=owner)
        try:
            project.delete(condition=cls._owned_by(owner))
        except DeleteError as exc:
            cls._raise_for_failed_condition(project_id, owner, exc)

    @staticmethod
    def _owned_by(owner: str) -> Condition:
        return ProjectEntity.pk.exists() & (ProjectEntity.project_owner == owner)

    @staticmethod
    def _raise_for_failed_condition(project_id: str, owner: str, exc: UpdateError | DeleteError) -> NoReturn:
        if exc.cause_response_code != "ConditionalCheckFailedException":
            raise exc
        ProjectQueryService().get_project(project_id, owner)
        raise ProjectForbiddenError from exc
