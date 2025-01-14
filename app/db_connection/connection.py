from abc import ABC, abstractmethod
from PIL import Image

class Connection(ABC):
    @abstractmethod
    def apply(self):
        """Метод для установления соединения с базой данных."""
        pass