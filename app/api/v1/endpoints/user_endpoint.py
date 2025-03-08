from fastapi import APIRouter, Depends

from app.core.cognito import Cognito
from app.core.dependencies import get_cognito
from app.services.user.get_service import get_users

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/")
async def show_users(cognito: Cognito = Depends(get_cognito)):
    users = get_users(cognito)

    return users
