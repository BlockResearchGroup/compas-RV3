from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__commandname__ = "RV3_pattern_attributes"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    AttributesForm.from_sceneNode(pattern)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
