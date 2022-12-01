from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_ui.objects import Group
from compas_rv3.datastructures import Pattern


__commandname__ = "RV3_pattern_from_lines"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    guids = compas_rhino.select_lines()
    if not guids:
        return

    lines = compas_rhino.get_line_coordinates(guids)
    pattern = Pattern.from_lines(lines, delete_boundary_face=True)

    if pattern.number_of_faces() == 0:
        compas_rhino.display_message("No faces found! Pattern object was not created.")
        return

    compas_rhino.rs.HideObjects(guids)

    group = ui.scene.add(Group(), name="RV3")
    group.add(pattern, name="Pattern")
    ui.scene.active_object = group
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
