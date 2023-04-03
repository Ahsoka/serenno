from enum import Enum


class ProductType(str, Enum):
    DESIGN = "DesignProductType"
    ANIMATION = "AnimationProductType"
    SIMULATION = "SimStudiesProductType"
    MANUFACTURE = "CAMProductType"
    DRAWING = "FusionDrawingProductType"


class WorkspaceEnum(str, Enum):
    DESIGN = "FusionSolidEnvironment"
    # NOTE: Have not tested GENERATIVE_DESIGN since I don't have access to it
    # id is sourced from this screenshot:
    # https://help.autodesk.com/cloudhelp/ENU/Fusion-360-API/images/UIExport1.png
    GENERATIVE_DESIGN = "GenerativeEnvironment"
    RENDER = "FusionRenderEnvironment"
    ANIMATION = "Publisher3DEnvironment"
    SIMULATION = "SimulationEnvironment"
    MANUFACTURE = "CAMEnvironment"
    DRAWING = "FusionDocumentationEnvironment"
    PCB = "PCBDesignEnvironement"


class WrongWorkspace(Exception):
    pass
