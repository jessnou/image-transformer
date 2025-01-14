import pytest
from httpx import AsyncClient
from app import main  # Импорт вашего FastAPI приложения
from PIL import Image
import io
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_upload_image():
    client = TestClient(main.app)
    with open("test_image.jpg", "rb") as file:
        response = client.post(
            "/upload-image/",
            files={"file": ("test_image.jpg", file, "image/png")}
        )
    assert response.status_code == 200
    json_response = response.json()
    assert "filename" in json_response
    assert "format" in json_response
    assert "size" in json_response
    assert "image_url" in json_response

@pytest.mark.asyncio
async def test_apply_adjustments():
    client = TestClient(main.app)
    with open("test_image.jpg", "rb") as file:
        response = client.post(
            "/apply-adjustments/",
            files={"file": ("test_image.jpg", file, "image/png")},
            data={"brightness": 1.2, "contrast": 1.5, "saturation": 1.3}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

@pytest.mark.asyncio
async def test_apply_adjustments_brightness_zero():
    client = TestClient(main.app)
    with open("test_image.jpg", "rb") as file:
        response = client.post(
            "/apply-adjustments/",
            files={"file": ("test_image.jpg", file, "image/png")},
            data={"brightness": 0.0, "contrast": 1.0, "saturation": 1.0}
        )
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"

    # Читаем результат как изображение
    image_data = io.BytesIO(response.content)
    image = Image.open(image_data)

    # Проверяем, что изображение полностью черное
    pixels = list(image.getdata())
    print(pixels)
    assert all(pixel == (0, 0, 0) for pixel in pixels), "Изображение должно быть полностью черным"