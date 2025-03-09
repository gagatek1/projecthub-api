from fastapi import FastAPI
from mangum import Mangum

from app.api.v1.router import router
from app.core.database import create_tables

app = FastAPI(
    title="ProjectHub API",
    description="API to manage projects and tasks",
    version="0.6.0",
)

handler = Mangum(app)

app.include_router(router)

create_tables()
