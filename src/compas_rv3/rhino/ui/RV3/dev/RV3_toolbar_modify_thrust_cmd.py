from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI

import RV3_thrust_modify_vertices_cmd
import RV3_thrust_move_supports_cmd
import RV3_thrust_modify_faces_cmd


__commandname__ = "RV3_toolbar_modify_thrust"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()
    thrust = ui.scene.active_object.get_child_by_name("ThrustDiagram")
    if not thrust:
        compas_rhino.display_message("No ThrustDiagram found in the active group.")
        return

    options = ["VerticesAttributes", "FacesAttributes", "MoveSupports"]
    option = compas_rhino.rs.GetString("Modify thrust diagram:", strings=options)

    if not option:
        return

    if option == "VerticesAttributes":
        RV3_thrust_modify_vertices_cmd.RunCommand(True)

    elif option == "FacesAttributes":
        RV3_thrust_modify_faces_cmd.RunCommand(True)

    elif option == "MoveSupports":
        RV3_thrust_move_supports_cmd.RunCommand(True)


if __name__ == "__main__":
    RunCommand(True)
