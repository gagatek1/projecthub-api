from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8)]


class UserVerify(BaseModel):
    email: EmailStr
    confirmation_code: Annotated[str, MaxLen(6)]


class UserSignin(BaseModel):
    email: EmailStr
    password: Annotated[str, MinLen(8)]


class UserRefreshToken(BaseModel):
    user_id: str
    refresh_token: str


class UserChangePassword(BaseModel):
    access_token: str
    old_password: Annotated[str, MinLen(8)]
    new_password: Annotated[str, MinLen(8)]


class UserForgotPassword(BaseModel):
    email: EmailStr


class UserConfirmForgotPassword(BaseModel):
    email: EmailStr
    confirmation_code: str
    new_password: Annotated[str, MinLen(8)]
