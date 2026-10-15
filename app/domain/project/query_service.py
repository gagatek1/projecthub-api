from app.domain.project.entity import ProjectEntity
from app.domain.project.exceptions import ProjectForbiddenError, ProjectNotFoundError
from app.domain.project.schemas import ProjectListResponse, ProjectResponse, ProjectSummaryResponse
from app.shared.pagination import decode_cursor, encode_cursor


class ProjectQueryService:
    def get_project(self, project_id: str, actor_id: str) -> ProjectResponse:
        pk = "project"
        sk = f"project#{project_id}"
        try:
            project = ProjectEntity.get(pk, sk)
        except ProjectEntity.DoesNotExist as exc:
            raise ProjectNotFoundError from exc
        if project.project_owner != actor_id:
            raise ProjectForbiddenError
        return ProjectResponse.model_validate(project)

    def list_projects(self, actor_id: str, limit: int, cursor: str | None = None) -> ProjectListResponse:
        pk = "project"
        projects = ProjectEntity.query(
            pk,
            filter_condition=ProjectEntity.project_owner == actor_id,
            limit=limit,
            last_evaluated_key=decode_cursor(cursor, pk=pk),
        )
        items = [ProjectSummaryResponse.model_validate(item) for item in projects]
        return ProjectListResponse(items=items, next_cursor=encode_cursor(projects.last_evaluated_key))
