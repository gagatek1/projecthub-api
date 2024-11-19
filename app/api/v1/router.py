from fastapi import APIRouter

from app.api.v1.endpoints.project_endpoint import project_router

router = APIRouter(prefix="/api/v1")

router.include_router(project_router)
