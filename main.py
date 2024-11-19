from fastapi import FastAPI
from mangum import Mangum

from app.api.v1.router import router
from app.core.database import create_tables

app = FastAPI()

handler = Mangum(app)

app.include_router(router)

create_tables()
