from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

import RV2pattern_modify_vertices_cmd
import RV2pattern_modify_edges_cmd
import RV2pattern_move_vertices_cmd
import RV2pattern_delete_cmd
import RV2pattern_relax_cmd
import RV2pattern_smooth_cmd


__commandname__ = "RV3_toolbar_modify_pattern"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        print("There is no Pattern in the scene.")
        return

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
        RV2pattern_modify_vertices_cmd.RunCommand(True)

    elif option == "EdgesAttributes":
        RV2pattern_modify_edges_cmd.RunCommand(True)

    elif option == "MoveVertices":
        RV2pattern_move_vertices_cmd.RunCommand(True)

    elif option == "DeleteVertices":
        RV2pattern_delete_cmd.RunCommand(True)

    elif option == "Relax":
        RV2pattern_relax_cmd.RunCommand(True)

    elif option == "Smooth":
        RV2pattern_smooth_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
