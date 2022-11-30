from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

__commandname__ = "RV3_pattern_smooth"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = get_object_by_name("Pattern")

    fixed = list(pattern.mesh.vertices_where(is_fixed=True))

    if not fixed:
        compas_rhino.display_message("Pattern has no fixed vertices! Smoothing requires fixed vertices.")
        return

    options = ["True", "False"]
    option = compas_rhino.rs.GetString("Press Enter to smooth or ESC to exit. Keep all boundaries fixed?", default=options[0], strings=options)

    if option is None:
        compas_rhino.display_message("Pattern smoothing aborted!")
        return

    if option == "True":
        fixed += list(flatten(pattern.mesh.vertices_on_boundaries()))

    pattern.mesh.smooth_area(fixed=fixed)

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
