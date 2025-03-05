from fastapi import APIRouter, Depends
from starlette import status

from app.core.security import get_token
from app.models.task import Task
from app.services.task.create_service import create_service
from app.services.task.delete_service import delete_service
from app.services.task.get_service import get_task, get_tasks
from app.services.task.update_service import update_service

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(task: Task, user: dict = Depends(get_token)):
    task = create_service(task, user)

    return task


@task_router.get("/")
async def show_tasks(user: dict = Depends(get_token)):
    tasks = get_tasks()

    return tasks


@task_router.get("/{task_id}")
async def show_task(task_id: str, user: dict = Depends(get_token)):
    task = get_task(task_id)

    return task


@task_router.delete("/delete/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: str, user: dict = Depends(get_token)):
    delete_service(task_id, user)


@task_router.put("/update")
async def update_project(task: Task, user: dict = Depends(get_token)):
    task = update_service(task, user)

    return task
