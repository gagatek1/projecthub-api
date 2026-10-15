from pydantic import BaseModel, ConfigDict

from app.shared.types import OpaqueToken, UserId


class RefreshTokenCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    user_id: UserId
    refresh_token: OpaqueToken
