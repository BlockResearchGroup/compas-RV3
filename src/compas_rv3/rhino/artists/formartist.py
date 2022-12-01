from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv3.artists import FormArtist
from .diagramartist import RhinoDiagramArtist


class RhinoFormArtist(RhinoDiagramArtist, FormArtist):
    """
    Rhino artist for RV3 form diagrams.
    """
