from pydantic import BaseModel, ConfigDict

from app.shared.types import Id, Name, Text, UserId


class UpdateTaskCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    project_id: Id
    task_id: Id
    actor_id: UserId
    name: Name
    description: Text
    assigned_user: UserId | None = None
