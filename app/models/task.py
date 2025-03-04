from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def generate_id():
    return str(uuid4())


class Task(BaseModel):
    id: str = Field(default_factory=generate_id)
    name: str
    description: str
    project_id: Optional[str] = None
    assigned_user: str
