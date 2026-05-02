from fastapi import FastAPI 
from contextlib import asynccontextmanager
from database   import init_db
from routers    import boards, posts

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db
    yield

app = FastAPI(lifespan = lifespan)

app.include_router(boards.router)
app.include_router(posts.router)