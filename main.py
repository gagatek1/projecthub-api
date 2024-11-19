from fastapi import FastAPI
from mangum import Mangum

from app.core.database import create_tables

app = FastAPI()

handler = Mangum(app)

create_tables()
