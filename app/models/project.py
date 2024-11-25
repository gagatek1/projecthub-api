from uuid import uuid4

from pydantic import BaseModel, Field


def generate_id():
    return str(uuid4())


class Project(BaseModel):
    id: str = Field(default_factory=generate_id)
    name: str
    description: str
    max_users: int
