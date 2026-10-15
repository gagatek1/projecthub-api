from .get import router as get_router
from .list import router as list_router
from .update_email import router as update_email_router

routers = [
    get_router,
    list_router,
    update_email_router,
]
