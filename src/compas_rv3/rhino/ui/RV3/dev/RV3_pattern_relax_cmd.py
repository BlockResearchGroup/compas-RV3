from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "RV3_pattern_relax"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = ui.scene.active_object.get_child_by_name("Pattern")
    if not pattern:
        compas_rhino.display_message("No Pattern found in the active group.")
        return

    fixed = list(pattern.mesh.vertices_where(is_fixed=True))

    if not fixed:
        compas_rhino.display_message("Pattern has no fixed vertices! Relaxation requires fixed vertices.")
        return

    fd_numpy = ui.proxy.function("compas.numerical.fd_numpy")

    vertex_index = pattern.mesh.key_index()
    xyz = pattern.mesh.vertices_attributes("xyz")
    loads = [[0.0, 0.0, 0.0] for _ in xyz]
    fixed[:] = [vertex_index[vertex] for vertex in fixed]
    edges = [(vertex_index[u], vertex_index[v]) for u, v in pattern.mesh.edges()]
    q = pattern.mesh.edges_attribute("q")

    xyz, q, f, l, r = fd_numpy(xyz, edges, fixed, q, loads)

    for vertex in pattern.mesh.vertices():
        index = vertex_index[vertex]
        pattern.mesh.vertex_attributes(vertex, "xyz", xyz[index])

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
