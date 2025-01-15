from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import base, transformation, users, transformation_history

app = FastAPI()

# Подключаем статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(base.router)
app.include_router(transformation.router)
app.include_router(users.router)
app.include_router(transformation_history.router)