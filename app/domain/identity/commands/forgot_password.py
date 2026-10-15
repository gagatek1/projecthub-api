from pydantic import BaseModel, ConfigDict

from app.shared.types import Email


class ForgotPasswordCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    email: Email
