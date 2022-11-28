from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__commandname__ = "RV3_form_relax"


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    form = scene.get("form")[0]
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    thrust = scene.get("thrust")[0]

    anchors = list(form.datastructure.vertices_where({"is_anchor": True}))
    fixed = list(form.datastructure.vertices_where({"is_fixed": True}))
    fixed = list(set(anchors + fixed))

    relax = proxy.function("compas.numerical.fd_numpy")

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

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
