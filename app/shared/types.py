from typing import Annotated

from pydantic import EmailStr, Field, StringConstraints

ID_PATTERN = r"^[A-Za-z0-9_-]{1,64}$"

Id = Annotated[str, StringConstraints(pattern=ID_PATTERN)]
Name = Annotated[str, StringConstraints(min_length=1, max_length=200)]
Text = Annotated[str, StringConstraints(max_length=10_000)]
Email = Annotated[EmailStr, StringConstraints(max_length=254)]
Password = Annotated[str, StringConstraints(min_length=8, max_length=256)]
ConfirmationCode = Annotated[str, StringConstraints(pattern=r"^\S{1,16}$")]
OpaqueToken = Annotated[str, StringConstraints(min_length=1, max_length=8192, pattern=r"^\S+$")]
PositiveCount = Annotated[int, Field(ge=1, le=100_000)]
UserId = Annotated[str, StringConstraints(min_length=1, max_length=128, pattern=r"^\S+$")]
