import pytest

from app.domain.project.command_handlers.create_project import create_project_handler
from app.domain.project.commands.create_project import CreateProjectCommand
from app.domain.project.query_service import ProjectQueryService

COMMAND = CreateProjectCommand(owner_id="alice", name="Apollo", description="Moon", max_users=3)


@pytest.mark.usefixtures("dynamodb")
class TestCreateProjectHandler:
    def test_persists_with_server_generated_id_and_owner(self) -> None:
        project = create_project_handler(COMMAND)

        assert project.project_owner == "alice"
        assert ProjectQueryService().get_project(project.id, "alice") == project

    def test_generates_distinct_ids(self) -> None:
        assert create_project_handler(COMMAND).id != create_project_handler(COMMAND).id
