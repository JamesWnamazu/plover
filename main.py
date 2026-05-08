import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from fastapi import FastAPI
from contextlib import asynccontextmanager
from db import init_db
from routers import boards, posts
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(boards.router)
app.include_router(posts.router)