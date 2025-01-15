from app.transformations.base import Transformation
from PIL import Image, ImageEnhance
from PIL import Image

from app.decorators.save_transformation import save_to_mongo


class AdjustmentClass(Transformation):
    def __init__(self, adjustments: dict):
        self.brightness = adjustments.get("brightness", 1.0)
        self.contrast = adjustments.get("contrast", 1.0)
        self.saturation = adjustments.get("saturation", 1.0)
        
    @save_to_mongo
    def apply(self, image: Image.Image) -> Image.Image:
        if self.brightness != 1.0:
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(self.brightness)
        if self.contrast != 1.0:
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(self.contrast)
        if self.saturation != 1.0:
            enhancer = ImageEnhance.Color(image)
            image = enhancer.enhance(self.saturation)
        return image
