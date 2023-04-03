from enum import Enum


class ProductType(str, Enum):
    DESIGN = "DesignProductType"
    ANIMATION = "AnimationProductType"
    SIMULATION = "SimStudiesProductType"
    MANUFACTURE = "CAMProductType"
    DRAWING = "FusionDrawingProductType"


class WrongWorkspace(Exception):
    pass
