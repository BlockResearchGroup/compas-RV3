from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI

__commandname__ = "RV3_form_relax"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    form = ui.scene.active_object.get_child_by_name("FormDiagram")
    if not form:
        compas_rhino.display_message("No FormDiagram found in the active group.")
        return

    thrust = ui.scene.active_object.get_child_by_name("ThrustDiagram")
    if not thrust:
        compas_rhino.display_message("No ThrustDiagram found in the active group.")
        return

    anchors = list(form.diagram.vertices_where(is_anchor=True))
    fixed = list(form.diagram.vertices_where(is_fixed=True))
    fixed = list(set(anchors + fixed))

    fd_numpy = ui.proxy.function("compas.numerical.fd_numpy")

    vertex_index = form.diagram.key_index()
    xyz = form.diagram.vertices_attributes("xyz")
    loads = [[0.0, 0.0, 0.0] for _ in xyz]
    fixed[:] = [vertex_index[vertex] for vertex in fixed]
    edges = [(vertex_index[u], vertex_index[v]) for u, v in form.diagram.edges()]

    q = form.diagram.edges_attribute("q")

    xyz, q, f, l, r = fd_numpy(xyz, edges, fixed, q, loads)

    for vertex in form.diagram.vertices():
        index = vertex_index[vertex]
        form.diagram.vertex_attributes(vertex, "xyz", xyz[index])

    if thrust:
        thrust.is_valid = False

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
