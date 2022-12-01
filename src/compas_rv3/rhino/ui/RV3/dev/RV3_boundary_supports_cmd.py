from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "RV3_boundary_supports"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = ui.scene.active_object.get_child_by_name("Pattern")
    if not pattern:
        compas_rhino.display_message("No pattern found in the active group.")
        return

    # mark all fixed vertices as anchors
    # mark all leaves as anchors

    fixed = list(pattern.mesh.vertices_where({"is_fixed": True}))
    leaves = []
    for vertex in pattern.mesh.vertices():
        nbrs = pattern.mesh.vertex_neighbors(vertex)
        count = 0
        for nbr in nbrs:
            if pattern.mesh.edge_attribute((vertex, nbr), "_is_edge"):
                count += 1
        if count == 1:
            leaves.append(vertex)

    anchors = list(set(fixed) | set(leaves))
    if anchors:
        pattern.mesh.vertices_attribute("is_anchor", True, keys=anchors)
        ui.scene.update()

    # manually Select or Unselect
    # should this not be included in the while loop?

    options = ["Select", "Unselect"]
    option1 = compas_rhino.rs.GetString("Select or unselect vertices as supports:", strings=options)

    if not option1:
        return

    options = ["AllBoundaryVertices", "Corners", "ByContinuousEdges", "Manual"]

    while True:
        option2 = compas_rhino.rs.GetString("Selection mode:", strings=options)

        if not option2:
            break

        if option2 == "AllBoundaryVertices":
            vertices = list(set(flatten(pattern.mesh.vertices_on_boundaries())))

        elif option2 == "Corners":
            angle = compas_rhino.rs.GetInteger("Angle tolerance for non-quad face corners:", 170, 1, 180)
            vertices = pattern.mesh.corner_vertices(tol=angle)

        elif option2 == "ByContinuousEdges":
            edges = pattern.select_edges()
            vertices = list(set(flatten([pattern.mesh.edge_loop_vertices(edge) for edge in edges])))

        elif option2 == "Manual":
            vertices = pattern.select_vertices()

        if vertices:
            pattern.select_vertex_points(vertices)

            if option1 == "Select":
                pattern.mesh.vertices_attribute("is_anchor", True, keys=vertices)
            else:
                pattern.mesh.vertices_attribute("is_anchor", False, keys=vertices)

        ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
