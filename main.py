from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database when the application starts
    await init_db()
    yield
    # Optionally, you can add cleanup code here if needed   

app = FastAPI(lifespan=lifespan)