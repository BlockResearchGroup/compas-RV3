from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI

import RV3_force_modify_vertices_cmd
import RV3_force_modify_edges_cmd
import RV3_force_move_vertices_cmd


__commandname__ = "RV3_toolbar_modify_force"


def RunCommand(is_interactive):

    ui = UI()
    force = ui.scene.active_object.get_child_by_name("ForceDiagram")
    if not force:
        compas_rhino.display_message("No ForceDiagram found in the active group.")
        return

    options = ["VerticesAttributes", "EdgesAttributes", "MoveVertices"]
    option = compas_rhino.rs.GetString("Modify force diagram:", strings=options)

    if not option:
        return

    if option == "VerticesAttributes":
        RV3_force_modify_vertices_cmd.RunCommand(True)

    elif option == "EdgesAttributes":
        RV3_force_modify_edges_cmd.RunCommand(True)

    elif option == "MoveVertices":
        RV3_force_move_vertices_cmd.RunCommand(True)


if __name__ == "__main__":
    RunCommand(True)
