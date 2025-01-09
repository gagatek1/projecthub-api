from pydantic import BaseModel


class Task(BaseModel):
    name: str
    description: str
    project: str
    assigned_user: str
