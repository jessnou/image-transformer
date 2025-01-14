from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from uuid import uuid4

from app.routers import base, transformation, users

app = FastAPI()

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(base.router)
app.include_router(transformation.router)
app.include_router(users.router)
