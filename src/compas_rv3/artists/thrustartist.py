from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv3.artists import DiagramArtist


class ThrustArtist(DiagramArtist):
    """
    Base artist for RV3 thrust diagrams.
    """

    def draw_selfweight(self, color, scale, tol=1e-3):
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
        raise NotImplementedError

    def draw_loads(self, color, scale, tol=1e-3):
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
        raise NotImplementedError

    def draw_reactions(self, color, scale, tol=1e-3):
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
        raise NotImplementedError

    def draw_residuals(self, color, scale, tol=1e-3):
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
        raise NotImplementedError

    # def draw_pipes(self, edges, color, scale, tol):
    #     vertex_xyz = self.vertex_xyz
    #     cylinders = []
    #     for edge in edges:
    #         u, v = edge
    #         start = vertex_xyz[u]
    #         end = vertex_xyz[v]
    #         force = self.mesh.edge_attribute(edge, "_f")
    #         force = scale * force
    #         if force < tol:
    #             continue
    #         radius = sqrt(force / pi)
    #         if isinstance(color, dict):
    #             pipe_color = color[edge]
    #         else:
    #             pipe_color = color
    #         cylinders.append(
    #             {"start": start, "end": end, "radius": radius, "color": pipe_color}
    #         )
    #     return compas_rhino.draw_cylinders(
    #         cylinders, layer=self.layer, clear=False, redraw=False
    #     )
