from pydantic import BaseModel, ConfigDict, SecretStr


class SignOutCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    access_token: SecretStr
