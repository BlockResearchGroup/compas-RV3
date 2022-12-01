from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from math import sqrt

import compas_rhino

from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import length_vector

from compas_rv3.artists import ThrustArtist
from .diagramartist import RhinoDiagramArtist


class RhinoThrustArtist(RhinoDiagramArtist, ThrustArtist):
    """
    Base artist for RV3 thrust diagrams.
    """

    def draw_selfweight(self, vertices, color, scale, tol=1e-3):
        """Draw the selfweight at each vertex of the diagram.

        Parameters
        ----------
        color : :class:`compas.colors.Color`
            The color of selfweight vectors.
        scale : float
            A scaling factor for the display of selfweight vectors.
        tol : float, optional
            A minimum length threshold after applying the scale factor.

        Returns
        -------
        list[guid]
            A list of guids corresponding to the line objects representing
            the selfweight vectors in Rhino.

        """
        vertex_xyz = self.vertex_xyz
        lines = []

        for vertex in vertices:
            area = self.mesh.vertex_tributary_area(vertex)
            thickness = self.mesh.vertex_attribute(vertex, "t")
            weight = area * thickness
            load = scale_vector((0, 0, 1), scale * weight)
            if length_vector(load) < tol:
                continue

            a = vertex_xyz[vertex]
            b = add_vectors(a, load)
            lines.append(
                {
                    "start": a,
                    "end": b,
                    "color": color.rgb255,
                    "arrow": "start",
                }
            )
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_loads(self, vertices, color, scale, tol=1e-3):
        """Draw the externally applied loads at all vertices of the diagram.

        Parameters
        ----------
        color : :class:`compas.colors.Color`
            The color of load vectors.
        scale : float
            A scaling factor for the display of loads.
        tol : float, optional
            A minimum length threshold after applying the scale factor.

        Returns
        -------
        list[guid]
            A list of guids corresponding to the line objects representing
            the load vectors in Rhino.

        """
        vertex_xyz = self.vertex_xyz
        lines = []

        for vertex in vertices:
            live = self.mesh.vertex_attribute(vertex, "pz")
            load = scale_vector((0, 0, 1), scale * live)
            if length_vector(load) < tol:
                continue

            a = vertex_xyz[vertex]
            b = add_vectors(a, load)
            lines.append(
                {
                    "start": a,
                    "end": b,
                    "color": color.rgb255,
                    "arrow": "start",
                }
            )
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_reactions(self, vertices, color, scale, tol=1e-3):
        """Draw the reaction forces at the anchored vertices of the diagram.

        Parameters
        ----------
        color : :class:`compas.colors.Color`
            The color of reaction forces.
        scale : float
            A scaling factor for the display of reaction force vectors.
        tol : float, optional
            A minimum length threshold after applying the scale factor.

        Returns
        -------
        list[guid]
            A list of guids corresponding to the line objects representing
            the reaction force vectors in Rhino.

        """
        vertex_xyz = self.vertex_xyz
        lines = []

        for vertex in vertices:
            r = self.mesh.vertex_attributes(vertex, ["_rx", "_ry", "_rz"])
            r = scale_vector(r, scale)
            if length_vector(r) < tol:
                continue

            a = vertex_xyz[vertex]
            b = add_vectors(a, r)
            lines.append(
                {
                    "start": a,
                    "end": b,
                    "color": color.rgb255,
                    "arrow": "start",
                }
            )
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_residuals(self, vertices, color, scale, tol=1e-3):
        """Draw the vertical component of the residual forces at the non-anchored vertices of the diagram.

        Parameters
        ----------
        color : :class:`compas.colors.Color`
            The color of residual force vectors.
        scale : float
            A scaling factor for the display of residual force vectors.
        tol : float, optional
            A minimum length threshold after applying the scale factor.

        Returns
        -------
        list[guid]
            A list of guids corresponding to the line objects representing
            the residual force vectors in Rhino.

        """
        vertex_xyz = self.vertex_xyz
        lines = []

        for vertex in vertices:
            r = self.mesh.vertex_attributes(vertex, ["_rx", "_ry", "_rz"])
            r = scale_vector(r, scale)
            if length_vector(r) < tol:
                continue

            a = vertex_xyz[vertex]
            b = add_vectors(a, r)
            lines.append(
                {
                    "start": a,
                    "end": b,
                    "color": color.rgb255,
                    "arrow": "start",
                }
            )
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_pipes(self, edges, color, scale, tol=1e-3):
        """Draw pipes representing the axial forces in the edges of the diagram.

        Parameters
        ----------
        color : :class:`compas.colors.Color`
            The color of the pipes.
        scale : float
            A scaling factor for the pipe radius.
        tol : float, optional
            A threshold for the size of the radius after applying the scaling factor.

        Returns
        -------
        list[guid]
            A list of guids corresponding to the pipe objects representing
            the axial forces in Rhino.

        """
        vertex_xyz = self.vertex_xyz
        cylinders = []

        for edge in edges:
            u, v = edge
            start = vertex_xyz[u]
            end = vertex_xyz[v]
            force = self.mesh.edge_attribute(edge, "_f")
            force = scale * force
            if force < tol:
                continue

            radius = sqrt(force / pi)
            if isinstance(color, dict):
                pipe_color = color[edge]
            else:
                pipe_color = color

            cylinders.append(
                {
                    "start": start,
                    "end": end,
                    "radius": radius,
                    "color": pipe_color.rgb255,
                }
            )
        return compas_rhino.draw_cylinders(cylinders, layer=self.layer, clear=False, redraw=False)
