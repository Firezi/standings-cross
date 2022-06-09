import logging
from fastapi import FastAPI
from tortoise import Tortoise

from src.db import init_db
from src import api

logger = logging.getLogger(__name__)
app = FastAPI()

app.include_router(api.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    await Tortoise.close_connections()
