from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import database
from app.models.users import User
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Роут для создания пользователя в PostgreSQL
@router.get("/users/add")
async def add_user_form(request: Request):
    return templates.TemplateResponse("users/add_user.html", {"request": request})

@router.post("/users")
def create_user(
    name: str = Form(...),
    email: str = Form(...),
    pg_session = Depends(database.get_postgres_session)
):
    new_user = User(name=name, email=email)
    pg_session.add(new_user)
    pg_session.commit()
    pg_session.refresh(new_user)
    return RedirectResponse(url="/users", status_code=303)


# Роут для получения списка всех пользователей
@router.get("/users")
def get_users(request: Request, pg_session = Depends(database.get_postgres_session)):
    users = pg_session.query(User).all()
    return templates.TemplateResponse("users/index.html", {"request": request, "users": users})

# Маршрут для смены пользователя
@router.post("/switch_user")
def switch_user(data: dict, session: Session = Depends(database.get_postgres_session)):
    user_id = data.get("user_id")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return JSONResponse({"user_name": user.name})


# # Роут для получения конкретного пользователя
# @router.get("/users/{user_id}")
# def get_user(user_id: int, pg_session = Depends(database.get_postgres_session())):
#     user = pg_session.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

# # Роут для обновления данных пользователя
# @router.put("/users/{user_id}")
# def update_user(
#     user_id: int,
#     user: UserCreate,
#     pg_session = Depends(database.get_postgres_session())
# ):
#     db_user = pg_session.query(User).filter(User.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     db_user.name = user.name
#     db_user.email = user.email
#     pg_session.commit()
#     pg_session.refresh(db_user)
#     return {"id": db_user.id, "name": db_user.name, "email": db_user.email}

# # Роут для удаления пользователя
# @router.delete("/users/{user_id}")
# def delete_user(user_id: int, pg_session = Depends(database.get_postgres_session())):
#     db_user = pg_session.query(User).filter(User.id == user_id).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     pg_session.delete(db_user)
#     pg_session.commit()
#     return {"detail": "User deleted"}