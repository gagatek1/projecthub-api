from pydantic import BaseModel, ConfigDict

from app.shared.types import Email, Password


class SignUpCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    email: Email
    password: Password
