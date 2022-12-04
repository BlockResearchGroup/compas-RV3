from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation

from compas_ui.values import Settings
from compas_ui.values import StrValue
from compas_ui.values import BoolValue
from compas_ui.values import ColorValue
from compas.colors import Color

from .diagramobject import DiagramObject


class ForceObject(DiagramObject):
    """
    Scene object for RV2 force diagrams.

    Attributes
    ----------
    vertex_xyz : dict[int, list[float, float, 0.0]]
        A dictionary mapping diagram vertices to their view coordinates.

    """

    SETTINGS = Settings(
        {
            "layer": StrValue("RV2::ForceDiagram"),
            "show.vertices": BoolValue(False),
            "show.edges": BoolValue(True),
            "color.vertices": ColorValue(Color.cyan()),
            "color.vertices:is_fixed": ColorValue(Color.cyan()),
            "color.edges": ColorValue(Color.blue()),
            "color.tension": ColorValue(Color.red()),
        }
    )

    @property
    def vertex_xyz(self):
        origin = Point(0, 0, 0)
        if self.anchor is not None:
            xyz = self.mesh.vertex_attributes(self.anchor, "xyz")
            point = Point(*xyz)
            T1 = Translation.from_vector(origin - point)
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T2 = Translation.from_vector(self.location)
            X = T2 * R * S * T1
        else:
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T = Translation.from_vector(self.location)
            X = T * R * S
        mesh = self.mesh.transformed(X)
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, "xy") + [0.0] for vertex in mesh.vertices()}
        return vertex_xyz
