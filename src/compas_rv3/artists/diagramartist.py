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
