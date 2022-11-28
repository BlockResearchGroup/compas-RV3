from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino


__commandname__ = "RV3_pattern_subdivide"


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

    options = ["Finer", "Coarser"]
    while True:

        option = compas_rhino.rs.GetString("Select mode", strings=options)

        if not option:
            break

        if option == "Finer":
            raise NotImplementedError

        elif option == "Coarser":
            raise NotImplementedError

        else:
            raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
