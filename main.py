from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, init_db

from routers.conversations import router as conversations_router
from routers.llm import router as llm_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(conversations_router)
app.include_router(llm_router)

@app.get("/")
async def healthy_check():
    return {"message": "Healthy"}