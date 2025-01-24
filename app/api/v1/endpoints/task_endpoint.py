from fastapi import APIRouter
from starlette import status

from app.models.task import Task
from app.services.task.create_service import create_service
from app.services.task.get_service import get_task, get_tasks

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    task = create_service(task)

    return task


@task_router.get("/")
async def show_tasks():
    tasks = get_tasks()

    return tasks


@task_router.get("/{task_id}")
async def show_task(task_id: str):
    task = get_task(task_id)

    return task
