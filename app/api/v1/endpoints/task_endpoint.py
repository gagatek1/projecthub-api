from fastapi import APIRouter
from starlette import status

from app.models.task import Task
from app.services.task.create_service import create_service
from app.services.task.delete_service import delete_service
from app.services.task.get_service import get_task, get_tasks
from app.services.task.update_service import update_service

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


@task_router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str):
    delete_service(task_id)

@task_router.put("/update")
async def update_project(task: Task):
    task = update_service(task)

    return task
