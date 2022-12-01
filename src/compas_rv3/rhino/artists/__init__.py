from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import plugin
from compas.artists import Artist

from compas_rv3.datastructures import FormDiagram
from compas_rv3.datastructures import ForceDiagram
from compas_rv3.datastructures import ThrustDiagram

from .diagramartist import RhinoDiagramArtist
from .formartist import RhinoFormArtist
from .forceartist import RhinoForceArtist
from .thrustartist import RhinoThrustArtist


@plugin(category="factories", requires=["Rhino"])
def register_artists():

    Artist.register(FormDiagram, RhinoFormArtist, context="Rhino")
    Artist.register(ForceDiagram, RhinoForceArtist, context="Rhino")
    Artist.register(ThrustDiagram, RhinoThrustArtist, context="Rhino")

    print("RV3 Rhino Artists registered.")


__all__ = [
    "RhinoDiagramArtist",
    "RhinoFormArtist",
    "RhinoForceArtist",
    "RhinoThrustArtist",
]
