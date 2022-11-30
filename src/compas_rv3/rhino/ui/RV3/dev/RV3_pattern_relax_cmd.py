from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

__commandname__ = "RV3_pattern_relax"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = get_object_by_name("Pattern")

    fixed = list(pattern.datastructure.vertices_where({"is_fixed": True}))

    if not fixed:
        compas_rhino.display_message("Pattern has no fixed vertices! Relaxation requires fixed vertices.")
        return

    relax = ui.proxy.function("compas.numerical.fd_numpy")

    key_index = pattern.datastructure.key_index()
    xyz = pattern.datastructure.vertices_attributes("xyz")
    loads = [[0.0, 0.0, 0.0] for _ in xyz]
    fixed[:] = [key_index[key] for key in fixed]
    edges = [(key_index[u], key_index[v]) for u, v in pattern.datastructure.edges()]

    q = pattern.datastructure.edges_attribute("q")

    xyz, q, f, l, r = relax(xyz, edges, fixed, q, loads)

    for key in pattern.datastructure.vertices():
        index = key_index[key]
        pattern.datastructure.vertex_attributes(key, "xyz", xyz[index])

    ui.scene.update()
    ui.record()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
