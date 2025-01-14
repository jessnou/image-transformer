from app.transformations.adjustments import AdjustmentClass
from app.transformations.base import Transformation
from app.transformations.filters import FilterClass
from app.transformations.style_transfer import StyleTransfer


class TransformationFactory:
    @staticmethod
    def create(transformation: dict) -> Transformation:
        if transformation["type"] == "style_transfer":
            return StyleTransfer(
                epochs=transformation.get("epochs", 100),
                content_weight=transformation.get("content_weight", 1),
                style_weight=transformation.get("style_weight", 1000),
                lr=transformation.get("lr", 0.01),
            )
        elif transformation["type"] == "filter":
            return FilterClass(transformation["filter"])
        elif transformation["type"] == "adjustments":
            return AdjustmentClass(transformation)
        else:
            raise ValueError(f"Unknown transformation type: {transformation['type']}")
