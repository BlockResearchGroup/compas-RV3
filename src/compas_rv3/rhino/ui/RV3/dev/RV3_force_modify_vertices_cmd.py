from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "RV3_force_modify_vertices"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    force = ui.scene.active_object.get_child_by_name("ForceDiagram")
    if not force:
        compas_rhino.display_message("No ForceDiagram found in the active group.")
        return

    thrust = ui.scene.active_object.get_child_by_name("ThrustDiagram")
    if not thrust:
        compas_rhino.display_message("No ThrustDiagram found in the active group.")
        return

    options = ["All", "ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "All":
        vertices = list(force.diagram.vertices())

    elif option == "ByContinuousEdges":
        edges = force.select_edges()
        vertices = list(set(flatten([force.diagram.edge_loop_vertices(edge) for edge in edges])))

    elif option == "Manual":
        vertices = force.select_vertices()

    if vertices:
        force.select_vertex_points(vertices)

        public = [name for name in force.diagram.default_vertex_attributes if not name.startswith("_")]
        if force.modify_vertices(vertices, names=public):
            if thrust:
                thrust.is_valid = False

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
