import pytest
from pynamodb.exceptions import PutError

from app.domain.project.entity import ProjectEntity
from app.domain.project.query_service import ProjectQueryService
from app.domain.project.repository import ProjectRepository
from tests.fixtures.factories import ProjectEntityFactory


@pytest.mark.usefixtures("dynamodb")
class TestProjectRepository:
    def test_create_never_overwrites_existing_project(self) -> None:
        project = ProjectEntityFactory.create()
        hijack = ProjectEntityFactory.build(id=project.id, project_owner="mallory")

        with pytest.raises(PutError):
            ProjectRepository.create(hijack)

        assert ProjectQueryService().get_project(project.id, "alice").project_owner == "alice"

    def test_create_inserts_new_project(self) -> None:
        project: ProjectEntity = ProjectEntityFactory.build()

        ProjectRepository.create(project)

        assert ProjectQueryService().get_project(project.id, "alice").id == project.id
