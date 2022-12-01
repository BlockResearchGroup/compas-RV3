from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.values import Settings
from compas_ui.values import StrValue
from compas_ui.values import BoolValue
from compas_ui.values import ColorValue
from compas_ui.values import IntValue
from compas.colors import Color


from compas_ui.objects import MeshObject


class PatternObject(MeshObject):
    """Scene object for patterns in RV2."""

    SETTINGS = Settings(
        {
            "layer": StrValue("RV2::Pattern"),
            "show.vertices": BoolValue(True),
            "show.edges": BoolValue(True),
            "show.faces": BoolValue(False),
            "color.vertices": ColorValue(Color.white()),
            "color.vertices:is_anchor": ColorValue(Color.red()),
            "color.vertices:is_fixed": ColorValue(Color.blue()),
            "color.vertices:is_constrained": ColorValue(Color.cyan()),
            "color.edges": ColorValue(Color.black()),
            "color.faces": ColorValue(Color.white().darkened(50)),
            "from_surface.density.U": IntValue(10),
            "from_surface.density.V": IntValue(10),
        }
    )
