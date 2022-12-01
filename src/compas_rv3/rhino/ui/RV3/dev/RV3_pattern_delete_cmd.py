from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "RV3_pattern_delete"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = ui.scene.active_object.get_child_by_name("Pattern")
    if not pattern:
        compas_rhino.display_message("No Pattern found in the active group.")
        return

    vertices = pattern.select_vertices()
    for vertex in vertices:
        if pattern.mesh.has_vertex(vertex):
            pattern.mesh.delete_vertex(vertex)

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
