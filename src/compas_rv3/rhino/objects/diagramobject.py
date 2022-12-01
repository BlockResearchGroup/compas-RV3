from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv3.objects import DiagramObject
from compas_ui.rhino.objects import RhinoMeshObject


class RhinoDiagramObject(RhinoMeshObject, DiagramObject):
    """
    Rhino scene object for diagrams in RV3.
    """
