from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "RV3_thrust_modify_faces"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    form = ui.scene.active_object.get_child_by_name("FormDiagram")
    if not form:
        compas_rhino.display_message("No FormDiagram found in the active group.")
        return

    thrust = ui.scene.active_object.get_child_by_name("ThrustDiagram")
    if not thrust:
        compas_rhino.display_message("No ThrustDiagram found in the active group.")
        return

    # hide the form vertices
    form_vertices = "{}::vertices".format(form.settings["layer"])
    compas_rhino.rs.HideGroup(form_vertices)
    # compas_rhino.rs.HideObjects(form.guid_face.keys())

    # selection options
    options = ["Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        ui.scene.update()
        return

    if option == "Manual":
        faces = thrust.select_faces()

    thrust_name = thrust.name

    if faces:
        thrust.select_face_meshes(faces)

        public = [name for name in form.diagram.default_face_attributes if not name.startswith("_")]
        if form.modify_faces(faces, names=public):
            thrust.diagram.data = form.diagram.data
            thrust.name = thrust_name
            thrust.is_valid = False

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
