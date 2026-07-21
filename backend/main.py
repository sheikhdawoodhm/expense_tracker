import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from contextlib import asynccontextmanager

load_dotenv()

# 2. NOW it is safe to import local files so they can read that database string
from src.db.tableCreation import init_db
from src.finance.router import router as finance_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="expense_tracker",
    version="1.0.0",
    lifespan=lifespan
)

origins = [
    "http://localhost:4200",  
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],   
)

app.include_router(finance_router)

@app.get("/health")
def check_health():
    return {"status": "healthy", "service": "finance-portfolio-api"}