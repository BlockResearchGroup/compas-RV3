from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv3.artists import ForceArtist
from .diagramartist import RhinoDiagramArtist


class RhinoForceArtist(RhinoDiagramArtist, ForceArtist):
    """
    Rhino artist for RV3 force diagrams.
    """
