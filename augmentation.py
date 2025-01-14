import albumentations as A
from PIL import Image
import numpy as np

# Поворот изображения на случайный угол
transform = A.RandomRotate90()

# Изменение яркости и контраста
transform = A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2)


# Чтение изображения
image = np.array(Image.open('app/static/73f162f2-9e7d-4f54-8da5-b29687cbd034.png'))

# Создание пайплайна для преобразований
transform = A.Compose([
    A.RandomRotate90(p=0.5),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),
    A.GaussianBlur(blur_limit=(5,5), p=1),
])

# Применение преобразований
augmented_image = transform(image=image)["image"]

# Отображение или сохранение преобразованного изображения
Image.fromarray(augmented_image).show()
