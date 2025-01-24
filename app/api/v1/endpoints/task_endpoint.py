from fastapi import APIRouter
from starlette import status

from app.models.task import Task
from app.services.task.create_service import create_service

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    task = create_service(task)

    return task
