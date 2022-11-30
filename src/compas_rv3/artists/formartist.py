from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv3.artists import DiagramArtist


class FormArtist(DiagramArtist):
    """
    Base artist for RV3 form diagrams.
    """

    @property
    def vertex_xyz(self):
        """dict:
        The view coordinates of the mesh vertices.
        The view coordinates default to the actual mesh coordinates.
        """
        if not self._vertex_xyz:
            self._vertex_xyz = {
                vertex: self.diagram.vertex_attributes(vertex, "xy") + [0.0] for vertex in self.diagram.vertices()
            }
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz
