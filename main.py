# TODO: Initialize packages in __init__.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import users
from core.databases.postgres.postgres import engine
from core.models import tables

load_dotenv()

app = FastAPI()
tables.Base.metadata.create_all(bind=engine)
origins = [
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

app.include_router(users.router)


@app.get("/")
async def health_check():
    return {"Health_check": "ok"}
