from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

# from compas_rv3.rhino import ModifyAttributesForm


__commandname__ = "RV3_force_modify_vertices"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    force = get_object_by_name("ForceDiagram")
    thrust = get_object_by_name("ThrustDiagram")

    options = ["All", "ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "All":
        keys = list(force.datastructure.vertices())

    elif option == "ByContinuousEdges":
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
        # current = scene.settings['RV2']['show.angles']
        # scene.settings['RV2']['show.angles'] = False
        # scene.update()

        # ModifyAttributesForm.from_sceneNode(force, 'vertices', keys)

        # scene.settings['RV2']['show.angles'] = current
        # if thrust:
        #     thrust.settings['_is.valid'] = False
        # scene.update()
        public = [
            name
            for name in force.datastructure.default_vertex_attributes.keys()
            if not name.startswith("_")
        ]
        if force.update_vertices_attributes(keys, names=public):
            if thrust:
                thrust.settings["_is.valid"] = False

    ui.scene.update()
    ui.record()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
