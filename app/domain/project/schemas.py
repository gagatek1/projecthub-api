from pydantic import BaseModel, ConfigDict

from app.shared.types import Name, PositiveCount, Text


class CreateProjectRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: Name
    description: Text
    max_users: PositiveCount


class UpdateProjectRequest(CreateProjectRequest):
    pass


class ProjectSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class ProjectResponse(ProjectSummaryResponse):
    description: str
    max_users: int
    project_owner: str


class ProjectListResponse(BaseModel):
    items: list[ProjectSummaryResponse]
    next_cursor: str | None
