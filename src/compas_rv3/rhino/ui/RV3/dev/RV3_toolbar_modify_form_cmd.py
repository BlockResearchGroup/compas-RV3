from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

import RV2form_attributes_cmd
import RV2form_modify_vertices_cmd
import RV2form_modify_edges_cmd
import RV2form_move_vertices_cmd
import RV2form_relax_cmd


__commandname__ = "RV3_toolbar_modify_form"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("form")[0]
    if not pattern:
        print("There is no FormDiagram in the scene.")
        return

    options = [
        "DiagramAttributes",
        "VerticesAttributes",
        "EdgesAttributes",
        "MoveVertices",
        "Relax",
    ]
    option = compas_rhino.rs.GetString("Modify form diagram:", strings=options)

    if not option:
        return

    if option == "DiagramAttributes":
        RV2form_attributes_cmd.RunCommand(True)

    elif option == "VerticesAttributes":
        RV2form_modify_vertices_cmd.RunCommand(True)

    elif option == "EdgesAttributes":
        RV2form_modify_edges_cmd.RunCommand(True)

    elif option == "MoveVertices":
        RV2form_move_vertices_cmd.RunCommand(True)

    elif option == "Relax":
        RV2form_relax_cmd.RunCommand(True)

    # elif option == "Smooth":
    #     RV2form_smooth_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
