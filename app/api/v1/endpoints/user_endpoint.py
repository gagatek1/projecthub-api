from fastapi import APIRouter, Depends

from app.core.cognito import Cognito
from app.core.dependencies import get_cognito
from app.models.user import UserEmail
from app.services.user.get_service import get_user, get_users
from app.services.user.update_service import get_token, update_email_service

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/")
async def show_users(cognito: Cognito = Depends(get_cognito)):
    users = get_users(cognito)

    return users


@user_router.get("/{user_id}")
async def show_user(user_id: str, cognito: Cognito = Depends(get_cognito)):
    user = get_user(user_id, cognito)

    return user


@user_router.post("/email")
async def update_email(
    email: UserEmail,
    user: dict = Depends(get_token),
    cognito: Cognito = Depends(get_cognito),
):
    return update_email_service(email, user, cognito)
