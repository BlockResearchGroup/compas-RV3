from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.datastructures import Pattern


__commandname__ = "RV3_pattern_from_lines"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    guids = compas_rhino.select_lines()
    if not guids:
        return

    lines = compas_rhino.get_line_coordinates(guids)
    pattern = Pattern.from_lines(lines, delete_boundary_face=True)

    if not pattern.face:
        print("No faces found! Pattern object was not created.")
        return

    compas_rhino.rs.HideObjects(guids)

    scene.clear()
    scene.add(pattern, name="pattern")
    scene.update()

    print("Pattern object successfully created.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
