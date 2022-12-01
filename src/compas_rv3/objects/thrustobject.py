from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas_ui.values import Settings
from compas_ui.values import StrValue
from compas_ui.values import BoolValue
from compas_ui.values import ColorValue
from compas_ui.values import FloatValue
from compas.colors import Color

from .diagramobject import DiagramObject


class ThrustObject(DiagramObject):
    """Scene object for thrust diagrams in RV2."""

    SETTINGS = Settings(
        {
            "layer": StrValue("RV2::ThrustDiagram"),
            "show.vertices": BoolValue(True),
            "show.edges": BoolValue(False),
            "show.faces": BoolValue(True),
            "show.stresses": BoolValue(False),
            "show.selfweight": BoolValue(False),
            "show.loads": BoolValue(False),
            "show.residuals": BoolValue(False),
            "show.reactions": BoolValue(True),
            "show.pipes": BoolValue(False),
            "color.vertices": ColorValue(Color.purple()),
            "color.vertices:is_fixed": ColorValue(Color.green()),
            "color.vertices:is_anchor": ColorValue(Color.red()),
            "color.edges": ColorValue(Color.purple()),
            "color.selfweight": ColorValue(Color.green().darkened(30)),
            "color.loads": ColorValue(Color.green().darkened(30)),
            "color.residuals": ColorValue(Color.cyan()),
            "color.reactions": ColorValue(Color.green().darkened(30)),
            "color.faces": ColorValue(Color.purple()),
            "color.pipes": ColorValue(Color.blue()),
            "color.invalid": ColorValue(Color.red().lightened(40)),
            "scale.selfweight": FloatValue(0.1),
            "scale.externalforces": FloatValue(0.1),
            "scale.residuals": FloatValue(1.0),
            "scale.pipes": FloatValue(0.01),
            "tol.selfweight": FloatValue(1e-3),
            "tol.externalforces": FloatValue(1e-3),
            "tol.residuals": FloatValue(1e-3),
            "tol.pipes": FloatValue(1e-3),
        }
    )

    def __init__(self, *args, **kwargs):
        super(ThrustObject, self).__init__(*args, **kwargs)
        self.is_valid = False
