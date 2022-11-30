from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name


__commandname__ = "RV3_thrust_modify_faces"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    form = get_object_by_name("FormDiagram")
    thrust = get_object_by_name("ThrustDiagram")

    if not form:
        print("There is no FormDiagram in the scene.")
        return

    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    # hide the form vertices
    form_vertices = "{}::vertices".format(form.settings["layer"])
    compas_rhino.rs.HideGroup(form_vertices)

    # selection options
    options = ["Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        ui.scene.update()
        return

    if option == "Manual":
        keys = thrust.select_faces()

    thrust_name = thrust.name

    if keys:
        public = [name for name in form.datastructure.default_face_attributes.keys() if not name.startswith("_")]
        if form.update_faces_attributes(keys, names=public):
            thrust.datastructure.data = form.datastructure.data
            thrust.name = thrust_name
            thrust.settings["_is.valid"] = False

    ui.scene.update()
    ui.record()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
