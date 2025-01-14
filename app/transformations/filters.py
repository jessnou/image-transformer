from app.transformations.base import Transformation
from PIL import Image, ImageOps, ImageEnhance
from PIL import Image


class FilterClass(Transformation):
    def __init__(self, filter_type: str):
        self.filter_type = filter_type

    def apply(self, image: Image.Image) -> Image.Image:
        if self.filter_type == "grayscale":
            return image.convert("L")
        elif self.filter_type == "sepia":
            image = ImageEnhance.Color(image).enhance(0.0)
            return ImageOps.colorize(image.convert("L"), "#704214", "#C0C0C0")
        elif self.filter_type == "invert":
            return ImageOps.invert(image.convert("RGB"))
        else:
            raise ValueError(f"Unknown filter type: {self.filter_type}")
