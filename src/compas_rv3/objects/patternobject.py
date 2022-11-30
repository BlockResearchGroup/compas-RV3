from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.objects import MeshObject


class PatternObject(MeshObject):
    """Scene object for patterns in RV2."""

    SETTINGS = {
        "layer": "RV2::Pattern",
        "show.vertices": True,
        "show.edges": True,
        "show.faces": False,
        "color.vertices": [255, 255, 255],
        "color.vertices:is_anchor": [255, 0, 0],
        "color.vertices:is_fixed": [0, 0, 255],
        "color.vertices:is_constrained": [0, 255, 255],
        "color.edges": [0, 0, 0],
        "color.faces": [200, 200, 200],
        "from_surface.density.U": 10,
        "from_surface.density.V": 10,
    }
