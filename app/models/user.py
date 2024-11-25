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
