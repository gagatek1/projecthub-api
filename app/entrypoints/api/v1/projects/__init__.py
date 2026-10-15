from .create import router as create_router
from .delete import router as delete_router
from .get import router as get_router
from .list import router as list_router
from .update import router as update_router

routers = [
    create_router,
    delete_router,
    get_router,
    list_router,
    update_router,
]
