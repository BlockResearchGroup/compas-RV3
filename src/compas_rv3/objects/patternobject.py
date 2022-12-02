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
from compas_ui.values import IntValue
from compas.colors import Color


from compas_ui.objects import MeshObject


class PatternObject(MeshObject):
    """
    Scene object for patterns in RV2.

    Attributes
    ----------
    vertex_xyz : dict[int, list[float, float, float]]
        A dictionary mapping pattern vertices to their view coordinates.

    """

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
        vertex_xyz = {vertex: mesh.vertex_attributes(vertex, "xyz") for vertex in mesh.vertices()}
        return vertex_xyz
