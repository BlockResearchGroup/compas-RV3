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
from compas_ui.values import FloatValue
from compas.colors import Color

from .diagramobject import DiagramObject


class ThrustObject(DiagramObject):
    """
    Scene object for thrust diagrams in RV2.

    Attributes
    ----------
    vertex_xyz : dict[int, list[float, float, float]]
        A dictionary mapping diagram vertices to their view coordinates.

    """

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
            "color.vertices:is_fixed": ColorValue(Color.blue()),
            "color.vertices:is_anchor": ColorValue(Color.red()),
            "color.edges": ColorValue(Color.purple()),
            "color.selfweight": ColorValue(Color.white()),
            "color.loads": ColorValue(Color.green().darkened(75)),
            "color.residuals": ColorValue(Color.cyan()),
            "color.reactions": ColorValue(Color.green().darkened(75)),
            "color.faces": ColorValue(Color.purple()),
            "color.pipes": ColorValue(Color.blue()),
            "color.invalid": ColorValue(Color.grey().lightened(75)),
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
