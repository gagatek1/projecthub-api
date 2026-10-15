from pydantic import BaseModel, ConfigDict, SecretStr

from app.shared.types import Email


class ChangeEmailCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    access_token: SecretStr
    email: Email
