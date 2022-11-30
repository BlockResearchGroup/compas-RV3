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

    vertex_index = pattern.datastructure.key_index()
    xyz = pattern.datastructure.vertices_attributes("xyz")
    loads = [[0.0, 0.0, 0.0] for _ in xyz]
    fixed[:] = [vertex_index[vertex] for vertex in fixed]
    edges = [(vertex_index[u], vertex_index[v]) for u, v in pattern.datastructure.edges()]
    q = pattern.datastructure.edges_attribute("q")

    xyz, q, f, l, r = fd_numpy(xyz, edges, fixed, q, loads)

    for vertex in pattern.datastructure.vertices():
        index = vertex_index[vertex]
        pattern.datastructure.vertex_attributes(vertex, "xyz", xyz[index])

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
