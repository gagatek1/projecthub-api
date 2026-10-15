from pydantic import BaseModel, ConfigDict, SecretStr

from app.shared.types import Password


class ChangePasswordCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    access_token: SecretStr
    old_password: Password
    new_password: Password
