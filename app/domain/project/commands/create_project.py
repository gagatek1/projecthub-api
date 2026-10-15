from pydantic import BaseModel, ConfigDict

from app.shared.types import Name, PositiveCount, Text, UserId


class CreateProjectCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    owner_id: UserId
    name: Name
    description: Text
    max_users: PositiveCount
