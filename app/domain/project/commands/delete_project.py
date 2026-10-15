from pydantic import BaseModel, ConfigDict

from app.shared.types import Id, UserId


class DeleteProjectCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    project_id: Id
    actor_id: UserId
