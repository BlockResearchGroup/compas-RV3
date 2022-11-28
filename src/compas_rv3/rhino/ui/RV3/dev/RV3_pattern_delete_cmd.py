from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__commandname__ = "RV3_pattern_delete"


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

    keys = pattern.select_vertices()
    for key in keys:
        if pattern.datastructure.has_vertex(key):
            pattern.datastructure.delete_vertex(key)
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
