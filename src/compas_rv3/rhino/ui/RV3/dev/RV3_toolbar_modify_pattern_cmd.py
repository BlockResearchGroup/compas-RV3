from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

import RV3_pattern_modify_vertices_cmd
import RV3_pattern_modify_edges_cmd
import RV3_pattern_move_vertices_cmd
import RV3_pattern_delete_cmd
import RV3_pattern_relax_cmd
import RV3_pattern_smooth_cmd


__commandname__ = "RV3_toolbar_modify_pattern"


@UI.error()
def RunCommand(is_interactive):

    get_object_by_name("Pattern")

    options = [
        "VerticesAttributes",
        "EdgesAttributes",
        "MoveVertices",
        "DeleteVertices",
        "Relax",
        "Smooth",
    ]
    option = compas_rhino.rs.GetString("Modify pattern:", strings=options)

    if not option:
        return

    if option == "VerticesAttributes":
        RV3_pattern_modify_vertices_cmd.RunCommand(True)

    elif option == "EdgesAttributes":
        RV3_pattern_modify_edges_cmd.RunCommand(True)

    elif option == "MoveVertices":
        RV3_pattern_move_vertices_cmd.RunCommand(True)

    elif option == "DeleteVertices":
        RV3_pattern_delete_cmd.RunCommand(True)

    elif option == "Relax":
        RV3_pattern_relax_cmd.RunCommand(True)

    elif option == "Smooth":
        RV3_pattern_smooth_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
