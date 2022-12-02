from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv3.artists import DiagramArtist


class ThrustArtist(DiagramArtist):
    """
    Base artist for RV3 thrust diagrams.
    """

    def draw_selfweight(self, vertices, color, scale, tol=1e-3):
        """Draw the selfweight at each vertex of the diagram.

        Parameters
        ----------
        vertices : list[int]
            The selection of vertices for which to draw the selfweight vectors.
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

    def draw_loads(self, vertices, color, scale, tol=1e-3):
        """Draw the externally applied loads at all vertices of the diagram.

        Parameters
        ----------
        vertices : list[int]
            The selection of vertices for which to draw the load vectors.
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

    def draw_reactions(self, vertices, color, scale, tol=1e-3):
        """Draw the reaction forces at the anchored vertices of the diagram.

        Parameters
        ----------
        vertices : list[int]
            The selection of vertices for which to draw the reaction forces.
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

    def draw_residuals(self, vertices, color, scale, tol=1e-3):
        """Draw the vertical component of the residual forces at the non-anchored vertices of the diagram.

        Parameters
        ----------
        vertices : list[int]
            The selection of vertices for which to draw the residual forces.
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

    def draw_pipes(self, edges, color, scale, tol=1e-3):
        """Draw pipes representing the axial forces in the edges of the diagram.

        Parameters
        ----------
        edges : list[tuple[int, int]]
            The selection of edges for which to draw the force pipes.
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
        raise NotImplementedError
