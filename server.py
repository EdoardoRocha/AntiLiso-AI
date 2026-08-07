from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.database import init
from routers import antiliso_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield


app = FastAPI(
    title="AntiLiso-AI-API",
    version="1.0.0",
    description="AntiLiso-AI-API",
    lifespan=lifespan,
)
app.include_router(antiliso_router.router)
