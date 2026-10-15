from pydantic import BaseModel, ConfigDict

from app.shared.types import ConfirmationCode, Email, Password


class ConfirmForgotPasswordCommand(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    email: Email
    confirmation_code: ConfirmationCode
    new_password: Password
