from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten


__commandname__ = "RV3_force_move_vertices"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    force = scene.get("force")[0]
    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    thrust = scene.get("thrust")[0]

    options = ["ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "ByContinuousEdges":
        temp = force.select_edges()
        keys = list(
            set(
                flatten(
                    [force.datastructure.vertices_on_edge_loop(key) for key in temp]
                )
            )
        )

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
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
