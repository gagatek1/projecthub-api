from pydantic import BaseModel, ConfigDict

from app.shared.types import Id, Name, PositiveCount, Text, UserId


class UpdateProjectCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    project_id: Id
    actor_id: UserId
    name: Name
    description: Text
    max_users: PositiveCount
