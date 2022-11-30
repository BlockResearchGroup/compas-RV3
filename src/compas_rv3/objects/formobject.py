from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.values import Settings
from compas_ui.values import StrValue
from compas_ui.values import BoolValue
from compas_ui.values import ColorValue
from compas.colors import Color


from compas_ui.objects import MeshObject


__all__ = ["FormObject"]


class FormObject(MeshObject):
    """Scene object for RV2 form diagrams.
    """

    SETTINGS = Settings({
        'layer': StrValue("RV2::FormDiagram"),
        'show.vertices': BoolValue(True),
        'show.edges': BoolValue(True),
        'color.vertices': ColorValue(Color.green()),
        'color.vertices:is_fixed': ColorValue(Color.blue()),
        'color.vertices:is_anchor': ColorValue(Color.white()),
        'color.edges': ColorValue(Color.green().darkened(50)),
        'color.tension': ColorValue(Color.red()),
        # 'input_guids': []
    })
