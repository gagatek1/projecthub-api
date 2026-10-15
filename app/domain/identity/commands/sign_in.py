from pydantic import BaseModel, ConfigDict

from app.shared.types import Email, Password


class SignInCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    email: Email
    password: Password
