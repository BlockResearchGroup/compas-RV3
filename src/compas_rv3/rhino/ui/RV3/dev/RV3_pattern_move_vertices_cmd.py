from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI


__commandname__ = "RV3_pattern_move_vertices"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    objects = ui.scene.get("Pattern")
    if not objects:
        compas_rhino.display_message("There is no Pattern in the scene.")
        return
    pattern = objects[0]

    options = ["ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "ByContinuousEdges":
        edges = pattern.select_edges()
        vertices = list(set(flatten([pattern.datastructure.vertices_on_edge_loop(edge) for edge in edges])))

    elif option == "Manual":
        vertices = pattern.select_vertices()

    if vertices:
        compas_rhino.rs.UnselectAllObjects()
        select_vertices(pattern, vertices)

        if pattern.move_vertices(vertices):
            ui.scene.update()
            ui.record()


if __name__ == "__main__":
    RunCommand(True)
