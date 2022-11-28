from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__commandname__ = "RV3_pattern_relax"


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    fixed = list(pattern.datastructure.vertices_where({"is_fixed": True}))

    if not fixed:
        print("Pattern has no fixed vertices! Relaxation requires fixed vertices.")
        return

    relax = proxy.function("compas.numerical.fd_numpy")

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

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
