from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv3.artists import DiagramArtist
from compas_ui.rhino.artists import MeshArtist as RhinoMeshArtist


class RhinoDiagramArtist(DiagramArtist, RhinoMeshArtist):
    """
    Rhino artist for diagrams in RhinoVAULT (3).
    """
