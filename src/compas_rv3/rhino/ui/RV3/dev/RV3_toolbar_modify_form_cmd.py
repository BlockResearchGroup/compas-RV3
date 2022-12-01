from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI

import RV3_form_modify_vertices_cmd
import RV3_form_modify_edges_cmd
import RV3_form_move_vertices_cmd
import RV3_form_relax_cmd


__commandname__ = "RV3_toolbar_modify_form"


def RunCommand(is_interactive):

    ui = UI()
    form = ui.scene.active_object.get_child_by_name("FormDiagram")
    if not form:
        compas_rhino.display_message("No FormDiagram found in the active group.")
        return

    options = ["VerticesAttributes", "EdgesAttributes", "MoveVertices", "Relax"]
    option = compas_rhino.rs.GetString("Modify form diagram:", strings=options)

    if not option:
        return

    if option == "VerticesAttributes":
        RV3_form_modify_vertices_cmd.RunCommand(True)

    elif option == "EdgesAttributes":
        RV3_form_modify_edges_cmd.RunCommand(True)

    elif option == "MoveVertices":
        RV3_form_move_vertices_cmd.RunCommand(True)

    elif option == "Relax":
        RV3_form_relax_cmd.RunCommand(True)


if __name__ == "__main__":
    RunCommand(True)
