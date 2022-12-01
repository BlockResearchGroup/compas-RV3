from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.values import Settings
from compas_ui.values import StrValue
from compas_ui.values import BoolValue
from compas_ui.values import ColorValue
from compas.colors import Color

from .diagramobject import DiagramObject


class ForceObject(DiagramObject):
    """Scene object for RV2 force diagrams."""

    SETTINGS = Settings(
        {
            "layer": StrValue("RV2::ForceDiagram"),
            "show.vertices": BoolValue(True),
            "show.edges": BoolValue(True),
            "color.vertices": ColorValue(Color.cyan()),
            "color.vertices:is_fixed": ColorValue(Color.cyan()),
            "color.edges": ColorValue(Color.blue()),
            "color.tension": ColorValue(Color.red()),
        }
    )

    @property
    def vertex_xyz(self):
        return {vertex: self.diagram.vertex_attributes(vertex, "xy") + [0.0] for vertex in self.diagram.vertices()}
