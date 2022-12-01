from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI

import RV3_boundary_supports_cmd
import RV3_boundary_boundaries_cmd


__commandname__ = "RV3_toolbar_boundary"


def RunCommand(is_interactive):

    ui = UI()
    pattern = ui.scene.active_object.get_child_by_name("Pattern")
    if not pattern:
        compas_rhino.display_message("No Pattern found in the active group.")
        return

    options = ["IdentifySupports", "UpdateBoundaries"]

    while True:
        option = compas_rhino.rs.GetString("Define boundary conditions:", strings=options)
        if not option:
            return

        if option == "IdentifySupports":
            RV3_boundary_supports_cmd.RunCommand(True)

        elif option == "UpdateBoundaries":
            RV3_boundary_boundaries_cmd.RunCommand(True)


if __name__ == "__main__":
    RunCommand(True)
