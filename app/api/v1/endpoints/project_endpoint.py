from fastapi import APIRouter, Depends
from starlette import status

from app.core.security import get_token
from app.models.project import Project
from app.services.project.create_service import create_service
from app.services.project.delete_service import delete_service
from app.services.project.get_service import get_project, get_projects
from app.services.project.update_service import update_service

project_router = APIRouter(prefix="/projects", tags=["projects"])


@project_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_project(project: Project, user: dict = Depends(get_token)):
    project = create_service(project, user)

    return project


@project_router.get("/")
async def show_projects(user: dict = Depends(get_token)):
    projects = get_projects()

    return projects


@project_router.get("/{project_id}")
async def show_project(project_id: str, user: dict = Depends(get_token)):
    project = get_project(project_id)

    return project


@project_router.delete("/delete/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: str, user: dict = Depends(get_token)):
    delete_service(project_id, user)


@project_router.put("/update")
async def update_project(project: Project, user: dict = Depends(get_token)):
    project = update_service(project, user)

    return project
