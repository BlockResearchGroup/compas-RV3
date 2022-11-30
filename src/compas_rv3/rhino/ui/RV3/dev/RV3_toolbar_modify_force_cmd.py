from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

import RV3_force_modify_vertices_cmd
import RV3_force_modify_edges_cmd
import RV3_force_move_vertices_cmd


__commandname__ = "RV3_toolbar_modify_force"


@UI.error()
def RunCommand(is_interactive):

    get_object_by_name("ForceDiagram")

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
