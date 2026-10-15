from pydantic import BaseModel, ConfigDict, Field

from app.shared.types import ConfirmationCode, Email, OpaqueToken, Password, UserId

_REQUEST = ConfigDict(extra="forbid")


class SignUpRequest(BaseModel):
    model_config = _REQUEST

    email: Email
    password: Password


class VerifyAccountRequest(BaseModel):
    model_config = _REQUEST

    email: Email
    confirmation_code: ConfirmationCode


class SignInRequest(BaseModel):
    model_config = _REQUEST

    email: Email
    password: Password


class RefreshTokenRequest(BaseModel):
    model_config = _REQUEST

    user_id: UserId = Field(description="Cognito username (sub in pools with email sign-in)")
    refresh_token: OpaqueToken


class ForgotPasswordRequest(BaseModel):
    model_config = _REQUEST

    email: Email


class ConfirmForgotPasswordRequest(BaseModel):
    model_config = _REQUEST

    email: Email
    confirmation_code: ConfirmationCode
    new_password: Password


class ChangePasswordRequest(BaseModel):
    model_config = _REQUEST

    old_password: Password
    new_password: Password


class ChangeEmailRequest(BaseModel):
    model_config = _REQUEST

    email: Email


class SignUpResponse(BaseModel):
    message: str = "User created successfully"
    sub: str


class TokenResponse(BaseModel):
    access_token: str = Field(serialization_alias="AccessToken")
    refresh_token: str | None = Field(default=None, serialization_alias="RefreshToken")
    expires_in: int = Field(serialization_alias="ExpiresIn")


class UserResponse(BaseModel):
    id: str
    sub: str | None
    status: str | None
    enabled: bool | None


class UserListResponse(BaseModel):
    items: list[UserResponse]
    next_cursor: str | None


class MessageResponse(BaseModel):
    message: str
