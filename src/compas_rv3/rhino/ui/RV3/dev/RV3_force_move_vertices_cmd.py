from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

__commandname__ = "RV3_force_move_vertices"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    force = get_object_by_name("ForceDiagram")
    thrust = get_object_by_name("ThrustDiagram")

    options = ["ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "ByContinuousEdges":
        temp = force.select_edges()
        keys = list(set(flatten([force.datastructure.vertices_on_edge_loop(key) for key in temp])))

    elif option == "Manual":
        keys = force.select_vertices()

    if keys:
        if force.move_vertices(keys):
            if force.datastructure.primal:
                force.datastructure.update_angle_deviations()
            if thrust:
                thrust.settings["_is.valid"] = False

    # the scene needs to be updated
    # even if the vertices where not modified
    # to reset group visibility to the configuration of settings
    ui.scene.update()
    ui.record()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
