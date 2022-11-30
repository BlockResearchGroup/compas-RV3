from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.values import Settings
from compas_ui.values import StrValue
from compas_ui.values import BoolValue
from compas_ui.values import ColorValue
from compas.colors import Color


from compas_ui.objects import MeshObject


__all__ = ["ForceObject"]


class ForceObject(MeshObject):
    """Scene object for RV2 force diagrams.
    """

    SETTINGS = Settings({
        'layer': StrValue("RV2::ForceDiagram"),
        'show.vertices': BoolValue(True),
        'show.edges': BoolValue(True),
        'color.vertices': ColorValue(Color.cyan()),
        'color.vertices:is_fixed': ColorValue(Color.cyan()),
        'color.edges': ColorValue(Color.blue()),
        'color.tension': ColorValue(Color.red())
    })
