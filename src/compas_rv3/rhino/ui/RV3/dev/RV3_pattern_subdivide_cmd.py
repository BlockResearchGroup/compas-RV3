from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name


__commandname__ = "RV3_pattern_subdivide"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = get_object_by_name("Pattern")

    options = ["Finer", "Coarser"]
    while True:

        option = compas_rhino.rs.GetString("Select mode", strings=options)

        if not option:
            break

        if option == "Finer":
            raise NotImplementedError

        elif option == "Coarser":
            raise NotImplementedError

        else:
            raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
