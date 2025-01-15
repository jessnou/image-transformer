from io import BytesIO
from bson import ObjectId
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import database
from PIL import Image

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/history")
async def history(request: Request, mongo_db=Depends(database.get_mongo_db)):
    images = list(mongo_db.images.find({}, {"image_data": 0}))
    
    # Convert ObjectId to string for JSON serialization
    for image in images:
        if "_id" in image:
            image["_id"] = str(image["_id"])
    
    return templates.TemplateResponse("history/index.html", {"request": request, "images": images})

# Роут для создания пользователя в PostgreSQL
@router.get("/image/{image_id}")
async def get_image(image_id: str, mongo_db=Depends(database.get_mongo_db)):
    # Ищем изображение по ID
    image_data = mongo_db.images.find_one({"_id": ObjectId(image_id)}, {"image_data": 1})

    if not image_data:
        raise HTTPException(status_code=404, detail="Изображение не найдено")

    # Преобразуем бинарные данные в изображение
    try:
        image_bytes = BytesIO(image_data["image_data"])
        image = Image.open(image_bytes)

        # Преобразуем изображение в байты
        output = BytesIO()
        image.save(output, format="PNG")  # Или "JPEG", если изображение в формате JPEG
        output.seek(0)

        # Возвращаем изображение как StreamingResponse
        return StreamingResponse(output, media_type="image/png")  # Или "image/jpeg"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке изображения: {e}")