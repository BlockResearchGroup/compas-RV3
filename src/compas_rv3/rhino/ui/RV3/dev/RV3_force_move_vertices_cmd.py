from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI


__commandname__ = "RV3_force_move_vertices"


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

    options = ["ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "ByContinuousEdges":
        temp = force.select_edges()
        keys = list(set(flatten([force.diagram.vertices_on_edge_loop(key) for key in temp])))

    elif option == "Manual":
        keys = force.select_vertices()

    if keys:
        if force.move_vertices(keys):
            if force.diagram.primal:
                force.diagram.update_angle_deviations()
            if thrust:
                thrust.settings["_is.valid"] = False

    # the scene needs to be updated
    # even if the vertices where not modified
    # to reset group visibility to the configuration of settings
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
