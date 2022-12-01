from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.artists import MeshArtist


class DiagramArtist(MeshArtist):
    """Base artist for diagrams in RhinoVAULT (3).

    Attributes
    ----------
    diagram : :class:`compas_rv3.datastructures.Diagram`
        The diagram associated with the artist.

    """

    @property
    def diagram(self):
        return self.mesh

    @diagram.setter
    def diagram(self, diagram):
        self.mesh = diagram

    @property
    def vertex_xyz(self):
        if not self._vertex_xyz:
            self._vertex_xyz = {vertex: self.diagram.vertex_attributes(vertex, "xy") + [0.0] for vertex in self.diagram.vertices()}
        return self._vertex_xyz

    @vertex_xyz.setter
    def vertex_xyz(self, vertex_xyz):
        self._vertex_xyz = vertex_xyz
