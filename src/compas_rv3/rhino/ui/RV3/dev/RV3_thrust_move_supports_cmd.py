from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI


__commandname__ = "RV3_thrust_move_supports"


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
    # compas_rhino.rs.HideObjects(form.guid_vertex.keys())

    # show the thrust vertices
    thrust_vertices_free = "{}::vertices_free".format(thrust.settings["layer"])
    thrust_vertices_anchor = "{}::vertices_anchor".format(thrust.settings["layer"])
    compas_rhino.rs.HideGroup(thrust_vertices_free)
    compas_rhino.rs.ShowGroup(thrust_vertices_anchor)
    # anchors = [guid for guid, vertex in thrust.guid_vertex.items() if thrust.diagram.vertex_attribute(vertex, "is_anchor")]
    # compas_rhino.rs.HideObjects(thrust.guid_vertex.keys())
    # compas_rhino.rs.ShowObjects(anchors)

    compas_rhino.rs.Redraw()

    # select anchored vertices
    vertices = thrust.select_vertices_anchor()

    if vertices:
        if thrust.move_vertices_direction(vertices, "z"):
            for vertex in vertices:
                # update the corresponding form diagram vertices
                z = thrust.diagram.vertex_attribute(vertex, "z")
                form.diagram.vertex_attribute(vertex, "z", z)
            thrust.is_valid = False

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
