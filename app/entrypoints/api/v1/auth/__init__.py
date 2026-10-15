from .change import router as change_router
from .confirm import router as confirm_router
from .forgot import router as forgot_router
from .logout import router as logout_router
from .signin import router as signin_router
from .signup import router as signup_router
from .token import router as token_router
from .verify import router as verify_router

routers = [
    change_router,
    confirm_router,
    forgot_router,
    logout_router,
    signin_router,
    signup_router,
    token_router,
    verify_router,
]
