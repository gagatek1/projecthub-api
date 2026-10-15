from pydantic import BaseModel, ConfigDict

from app.shared.types import Id, UserId


class DeleteTaskCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    project_id: Id
    task_id: Id
    actor_id: UserId
