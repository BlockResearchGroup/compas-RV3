from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name


__commandname__ = "RV3_pattern_delete"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = get_object_by_name("Pattern")

    vertices = pattern.select_vertices()
    for vertex in vertices:
        if pattern.datastructure.has_vertex(vertex):
            pattern.datastructure.delete_vertex(vertex)

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
