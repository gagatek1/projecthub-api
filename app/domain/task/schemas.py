from pydantic import BaseModel, ConfigDict

from app.shared.types import Name, Text, UserId


class CreateTaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    name: Name
    description: Text
    assigned_user: UserId | None = None


class UpdateTaskRequest(CreateTaskRequest):
    pass


class TaskSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class TaskResponse(TaskSummaryResponse):
    description: str
    project_id: str
    assigned_user: str


class TaskListResponse(BaseModel):
    items: list[TaskSummaryResponse]
    next_cursor: str | None
