from fastapi import APIRouter
from starlette import status

from app.models.project import Project
from app.services.project.create_service import create_service
from app.services.project.get_service import get_projects

project_router = APIRouter(prefix="/projects", tags=["projects"])


@project_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_project(project: Project):
    project = create_service(project)

    return project


@project_router.get("/")
async def show_projects():
    projects = get_projects()

    return projects
