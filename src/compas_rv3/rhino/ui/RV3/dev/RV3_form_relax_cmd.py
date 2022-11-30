from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

__commandname__ = "RV3_form_relax"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    form = get_object_by_name("FormDiagram")
    thrust = get_object_by_name("ThrustDiagram")

    anchors = list(form.datastructure.vertices_where({"is_anchor": True}))
    fixed = list(form.datastructure.vertices_where({"is_fixed": True}))
    fixed = list(set(anchors + fixed))

    relax = ui.proxy.function("compas.numerical.fd_numpy")

    key_index = form.datastructure.key_index()
    xyz = form.datastructure.vertices_attributes("xyz")
    loads = [[0.0, 0.0, 0.0] for _ in xyz]
    fixed[:] = [key_index[key] for key in fixed]
    edges = [(key_index[u], key_index[v]) for u, v in form.datastructure.edges()]

    q = form.datastructure.edges_attribute("q")

    xyz, q, f, l, r = relax(xyz, edges, fixed, q, loads)

    for key in form.datastructure.vertices():
        index = key_index[key]
        form.datastructure.vertex_attributes(key, "xyz", xyz[index])

    if thrust:
        thrust.settings["_is.valid"] = False

    ui.scene.update()
    ui.record()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
