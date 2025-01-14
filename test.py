import os
from uuid import uuid4
from PIL import Image, ImageOps, ImageEnhance
from PIL import Image
import numpy as np
import torch
from matplotlib import pyplot as plt

from app.factories.transformation_factory import TransformationFactory

img = Image.open('app/static/right.jpg').convert('RGB')
img_style = Image.open('app/static/img_style.jpg').convert('RGB')

style_transfer = TransformationFactory.create({
    "type": "style_transfer",
    "epochs": 10
})

result_image = style_transfer.apply(img, img_style)

result_image.show()