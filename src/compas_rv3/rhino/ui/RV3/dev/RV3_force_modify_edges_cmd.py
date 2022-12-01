from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "RV3_force_modify_edges"


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

    options = ["All", "Continuous", "Parallel", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "All":
        edges = list(force.diagram.edges())

    elif option == "Continuous":
        edges = force.select_edges()
        edges = list(set(flatten([force.diagram.edge_loop(edge) for edge in edges])))

    elif option == "Parallel":
        edges = force.select_edges()
        edges = list(set(flatten([force.diagram.edge_strip(edge) for edge in edges])))

    elif option == "Manual":
        edges = force.select_edges()

    if edges:
        force.select_edge_lines(edges)

        public = [name for name in force.diagram.default_edge_attributes if not name.startswith("_")]
        if force.modify_edges(edges, names=public):
            if thrust:
                thrust.is_valid = False

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
