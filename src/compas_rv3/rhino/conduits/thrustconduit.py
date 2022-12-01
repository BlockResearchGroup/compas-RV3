from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.conduits import BaseConduit

from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import scale_vector

# from compas.geometry import centroid_points
# from compas.geometry import dot_vectors
from compas.geometry import length_vector_sqrd

from System.Drawing.Color import FromArgb
from Rhino.Geometry import Line
from Rhino.Geometry import Point3d


class SelfWeightConduit(BaseConduit):
    """Display conduit for ThrustDiagram selfweight.

    Parameters
    ----------
    mesh : :class:`compas_rv2.datastructures.ThrustDiagram`
        The thrust diagram.
    color : rgb tuple
        The color of the reaction forces.
    scale : float
        The scale factor.
    tol : float
        Minimum length of a reaction force vector.
    """

    def __init__(self, diagram, color, scale=1.0, tol=1e-3, **kwargs):
        super(SelfWeightConduit, self).__init__(**kwargs)
        self.diagram = diagram
        self.color = color
        self.scale = scale
        self.tol = tol

    def PostDrawObjects(self, e):
        color = FromArgb(*self.color)
        lines = []
        for vertex in self.diagram.vertices():
            area = self.diagram.vertex_tributary_area(vertex)
            thickness = self.diagram.vertex_attribute(vertex, "t")
            weight = area * thickness * self.scale
            if weight < self.tol:
                continue

            start = self.diagram.vertex_coordinates(vertex)
            end = [start[0], start[1], start[2] - weight]
            end = [start[0], start[1], start[2] - weight]
            line = Line(Point3d(*start), Point3d(*end))
            lines.append(line)
        if lines:
            e.Display.DrawArrows(lines, color)


class ReactionConduit(BaseConduit):
    """Display conduit for ThrustDiagram reactions.

    Parameters
    ----------
    mesh : :class:`compas_rv2.datastructures.ThrustDiagram`
        The thrust diagram.
    color : rgb tuple
        The color of the reaction forces.
    scale : float
        The scale factor.
    tol : float
        Minimum length of a reaction force vector.
    """

    def __init__(self, diagram, color, scale=1.0, tol=1e-3, **kwargs):
        super(ReactionConduit, self).__init__(**kwargs)
        self.diagram = diagram
        self.color = color
        self.scale = scale
        self.tol = tol

    def PostDrawObjects(self, e):
        color = FromArgb(*self.color)
        scale = self.scale
        tol2 = self.tol**2
        mesh = self.diagram
        lines = []
        for vertex in mesh.vertices_where(is_anchor=True):
            reaction = mesh.vertex_attributes(vertex, ["_rx", "_ry", "_rz"])
            reaction = scale_vector(reaction, -scale)
            if length_vector_sqrd(reaction) < tol2:
                continue

            start = mesh.vertex_attributes(vertex, "xyz")
            end = subtract_vectors(start, reaction)
            line = Line(Point3d(*end), Point3d(*start))
            lines.append(line)
        if lines:
            e.Display.DrawArrows(lines, color)


class LoadConduit(BaseConduit):
    """Display conduit for ThrustDiagram loads.

    Parameters
    ----------
    mesh : :class:`compas_rv2.datastructures.ThrustDiagram`
        The thrust diagram.
    color : rgb tuple
        The color of the reaction forces.
    scale : float
        The scale factor.
    tol : float
        Minimum length of a reaction force vector.
    """

    def __init__(self, diagram, color, scale=1.0, tol=1e-3, **kwargs):
        super(LoadConduit, self).__init__(**kwargs)
        self.diagram = diagram
        self.color = color
        self.scale = scale
        self.tol = tol

    def PostDrawObjects(self, e):
        color = FromArgb(*self.color)
        scale = self.scale
        tol2 = self.tol**2
        lines = []
        for vertex in self.cablemesh.vertices():
            start = self.cablemesh.vertex_coordinates(vertex)
            load = self.cablemesh.vertex_attributes(vertex, ["px", "py", "pz"])
            load = scale_vector(load, scale)
            if length_vector_sqrd(load) < tol2:
                continue
            end = add_vectors(start, load)
            line = Line(Point3d(*start), Point3d(*end))
            lines.append(line)
        if lines:
            e.Display.DrawArrows(lines, color)


class ResidualConduit(BaseConduit):
    """Display conduit for ThrustDiagram residuals.

    Parameters
    ----------
    mesh : :class:`compas_rv2.datastructures.ThrustDiagram`
        The thrust diagram.
    color : rgb tuple
        The color of the reaction forces.
    scale : float
        The scale factor.
    tol : float
        Minimum length of a reaction force vector.
    """

    def __init__(self, diagram, color, scale=1.0, tol=1e-3, **kwargs):
        super(ResidualConduit, self).__init__(**kwargs)
        self.diagram = diagram
        self.color = color
        self.scale = scale
        self.tol = tol

    def PostDrawObjects(self, e):
        color = FromArgb(*self.color)
        scale = self.scale
        tol2 = self.tol**2
        mesh = self.diagram
        lines = []
        for vertex in mesh.vertices_where(is_anchor=False):
            reaction = mesh.vertex_attributes(vertex, ["_rx", "_ry", "_rz"])
            reaction = scale_vector(reaction, -scale)
            if length_vector_sqrd(reaction) < tol2:
                continue

            end = mesh.vertex_attributes(vertex, "xyz")
            start = subtract_vectors(end, reaction)
            line = Line(Point3d(*end), Point3d(*start))
            lines.append(line)
        if lines:
            e.Display.DrawArrows(lines, color)
