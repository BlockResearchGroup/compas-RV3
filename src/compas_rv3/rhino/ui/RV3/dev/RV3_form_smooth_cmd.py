from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name


__commandname__ = "RV3_form_smooth"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    form = get_object_by_name("FormDiagram")
    thrust = get_object_by_name("ThrustDiagram")

    anchors = list(form.diagram.vertices_where(is_anchor=True))
    fixed = list(form.diagram.vertices_where(is_fixed=True))
    fixed = anchors + fixed

    options = ["True", "False"]
    option = compas_rhino.rs.GetString("Press Enter to smooth or ESC to exit. Keep all boundaries fixed?", options[0], options)

    if option is None:
        compas_rhino.display_message("Form smoothing aborted!")
        return

    if option == "True":
        fixed += list(flatten(form.diagram.vertices_on_boundaries()))
        fixed += list(flatten([form.diagram.face_vertices(face) for face in form.diagram.faces_where({"_is_loaded": False})]))

    fixed = list(set(fixed))

    form.diagram.smooth_area(fixed=fixed)

    if thrust:
        thrust.settings["_is.valid"] = False

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
