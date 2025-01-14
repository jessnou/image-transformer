from abc import ABC, abstractmethod
from PIL import Image

class Transformation(ABC):
    @abstractmethod
    def apply(self, image: Image.Image) -> Image.Image:
        pass
