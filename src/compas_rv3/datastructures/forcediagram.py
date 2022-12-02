from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import angle_vectors_xy
from compas.geometry import cross_vectors

from compas_tna.diagrams import ForceDiagram
from compas_rv3.datastructures.diagram import Diagram


class ForceDiagram(Diagram, ForceDiagram):
    """
    Data structure for force diagrams.
    """

    def primal_edge(self, edge):
        """
        Get the corresponding edge in the FormDiagram.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge in this diagram.

        Returns
        -------
        tuple[int, int]
            The identifier of the edge in the other/primal diagram.

        Raises
        ------
        KeyError
            If the dual edge does not exist.

        """
        f1, f2 = edge
        for u, v in self.primal.face_halfedges(f1):
            if self.primal.halfedge[v][u] == f2:
                return u, v
        raise KeyError(edge)

    def update_angle_deviations(self):
        """
        Compute the angle deviation with the corresponding edge in the FormDiagram.

        Returns
        -------
        None

        """
        for edge in self.edges():
            edge_ = self.primal_edge(edge)
            uv = self.edge_vector(*edge)
            uv_ = self.primal.edge_vector(*edge_)
            a = angle_vectors_xy(uv, cross_vectors(uv_, (0, 0, 1)), deg=True)
            if self.primal.edge_attribute(edge_, "_is_tension"):
                a = 180 - a
            self.edge_attribute(edge, "_a", a)
            self.primal.edge_attribute(edge_, "_a", a)
