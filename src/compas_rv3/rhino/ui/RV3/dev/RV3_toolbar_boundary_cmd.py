from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

import RV3_boundary_supports_cmd
import RV3_boundary_boundaries_cmd


__commandname__ = "RV3_toolbar_boundary"


@UI.error()
def RunCommand(is_interactive):

    get_object_by_name("Pattern")

    options = ["IdentifySupports", "UpdateBoundaries"]

    while True:
        option = compas_rhino.rs.GetString(
            "Define boundary conditions:", strings=options
        )
        if not option:
            return

        if option == "IdentifySupports":
            RV3_boundary_supports_cmd.RunCommand(True)

        elif option == "UpdateBoundaries":
            RV3_boundary_boundaries_cmd.RunCommand(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
