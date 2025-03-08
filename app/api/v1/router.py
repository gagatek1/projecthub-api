from fastapi import APIRouter

from app.api.v1.endpoints.auth_endpoint import auth_router
from app.api.v1.endpoints.project_endpoint import project_router
from app.api.v1.endpoints.task_endpoint import task_router
from app.api.v1.endpoints.user_endpoint import user_router

router = APIRouter(prefix="/api/v1")

router.include_router(project_router)
router.include_router(auth_router)
router.include_router(task_router)
router.include_router(user_router)
