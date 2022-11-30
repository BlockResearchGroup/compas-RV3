from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI


__commandname__ = "RV3_pattern_modify_vertices"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    objects = ui.scene.get("Pattern")
    if not objects:
        compas_rhino.display_message("There is no Pattern in the scene.")
        return
    pattern = objects[0]

    options = ["AllBoundaryVertices", "Corners", "ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection mode:", strings=options)

    if not option:
        return

    if option == "AllBoundaryVertices":
        vertices = pattern.datastructure.vertices_on_boundary()

    elif option == "Corners":
        angle = compas_rhino.rs.GetInteger("Angle tolerance for non-quad face corners:", 170, 1, 180)
        vertices = pattern.datastructure.corner_vertices(tol=angle)

    elif option == "ByContinuousEdges":
        edges = pattern.select_edges()
        vertices = list(set(flatten([pattern.datastructure.vertices_on_edge_loop(edge) for edge in edges])))

    elif option == "Manual":
        vertices = pattern.select_vertices()

    if vertices:
        public = [name for name in pattern.datastructure.default_vertex_attributes if not name.startswith("_")]
        if pattern.update_vertices_attributes(vertices, names=public):
            ui.scene.update()
            ui.record()


if __name__ == "__main__":
    RunCommand(True)
