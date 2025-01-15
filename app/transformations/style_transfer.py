from app.nn_models.vgg_style_transfer import transfer_style
from app.decorators.save_transformation import save_to_mongo
from .base import Transformation
from PIL import Image
import numpy as np

class StyleTransfer(Transformation):
    def __init__(self, epochs=100, content_weight=1, style_weight=1000, lr=0.01):
        self.epochs = epochs
        self.content_weight = content_weight
        self.style_weight = style_weight
        self.lr = lr

    @save_to_mongo
    def apply(self, content_image: Image.Image, style_image: Image.Image) -> Image.Image:
        result_tensor = transfer_style(
            content_image, style_image,
            epochs=self.epochs,
            content_weight=self.content_weight,
            style_weight=self.style_weight,
            lr=self.lr
        )

        # Преобразуем тензор обратно в изображение
        result_image = self.tensor_to_image(result_tensor)
        return result_image

    def tensor_to_image(self, tensor):
        tensor = tensor.detach().squeeze()
        tensor = (tensor - tensor.min()) / (tensor.max() - tensor.min()) * 255.0
        tensor = tensor.permute(1, 2, 0).numpy().astype(np.uint8)
        return Image.fromarray(tensor)
