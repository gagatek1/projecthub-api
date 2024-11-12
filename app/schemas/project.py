from pydantic import BaseModel

class Project(BaseModel):
    id: int
    name: str
    description: str
    max_users: int
