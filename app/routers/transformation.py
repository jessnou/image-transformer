from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from fastapi import Form, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image, ImageOps, ImageEnhance
from PIL import Image
import io
import os
from uuid import uuid4

from app.factories.transformation_factory import TransformationFactory
from app.decorators.save_transformation import save_to_mongo

router = APIRouter()

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Читаем изображение
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Сохраняем изображение на сервере
        filename = f"{uuid4()}.png"
        image_path = os.path.join("app/static", filename)
        image.save(image_path)

        # Возвращаем информацию о загруженном изображении
        return JSONResponse(content={
            "filename": file.filename,
            "format": image.format,
            "size": {"width": image.width, "height": image.height},
            "image_url": f"/static/{filename}"
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@router.post("/apply-adjustments/")
@save_to_mongo
async def apply_adjustments(
    file: UploadFile = File(...),
    brightness: float = Form(...),
    contrast: float = Form(...),
    saturation: float = Form(...)
):
    try:
        # Читаем изображение
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        transformation = TransformationFactory.create(
            {
                "type": 'adjustments',
                "brightness": brightness,
                "contrast": contrast,
                "saturation": saturation,
            }
        ) 
        image = transformation.apply(image)

        # Конвертируем изображение в байты
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        # Возвращаем изображение как StreamingResponse
        return StreamingResponse(image_bytes, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}

@router.post("/apply-filter/")
@save_to_mongo 
async def apply_filter(file: UploadFile = File(...), filter: str = Form(...)):
    try:
        # Читаем изображение
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        transformation = TransformationFactory.create(
            {
                "type": 'filter',
                "filter": filter,
            }
        ) 
        image = transformation.apply(image)

        # Сохраняем отфильтрованное изображение
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        # Возвращаем изображение как StreamingResponse
        return StreamingResponse(image_bytes, media_type="image/png")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    

@router.post("/apply-transformations/")
@save_to_mongo 
async def apply_transformations(
    file: UploadFile = File(...),
    transformations: str = Form(...)
):
    try:
        # Читаем изображение
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))

        # Преобразуем список трансформаций
        transformations_list = eval(transformations)  # Преобразуем JSON-строку в список
        transformation_objects = [
            TransformationFactory.create(transformation) for transformation in transformations_list
        ]

        # Применяем трансформации
        for transformation in transformation_objects:
            image = transformation.apply(image)

        
        # Сохраняем отфильтрованное изображение
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        # Возвращаем изображение как StreamingResponse
        return StreamingResponse(image_bytes, media_type="image/png")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)


@router.post("/apply-style-transfer/")
@save_to_mongo 
async def style_transfer(
    content_file: UploadFile = File(...),
    style_file: UploadFile = File(...),
    epochs: int = Form(100),
    content_weight: float = Form(1.0),
    style_weight: float = Form(1000.0),
    lr: float = Form(0.01)
):
    try:
        content_data = await content_file.read()
        style_data = await style_file.read()
        content_image = Image.open(io.BytesIO(content_data)).convert("RGB")
        style_image = Image.open(io.BytesIO(style_data)).convert("RGB")

        style_transfer = TransformationFactory.create({
            "type": "style_transfer",
            "epochs": epochs,
            "content_weight": content_weight,
            "style_weight": style_weight,
            "lr": lr
        })

        result_image = style_transfer.apply(content_image, style_image)
        
        # Сохраняем отфильтрованное изображение
        image_bytes = io.BytesIO()
        result_image.save(image_bytes, format="PNG")
        image_bytes.seek(0)

        # Возвращаем изображение как StreamingResponse
        return StreamingResponse(image_bytes, media_type="image/png")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)