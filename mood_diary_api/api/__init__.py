from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import config
from .db import DB, BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    DB(config.mysql_dsn)
    if config.debug:
        await DB.drop_all()
        print('API starts in dev mode! All DB columns dropped!')
    await DB.create_all()
    yield


api = FastAPI(lifespan=lifespan)
