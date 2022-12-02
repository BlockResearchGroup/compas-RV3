from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino
from compas_ui.ui import UI

__commandname__ = "RV3_thrust_modify_vertices"


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
    compas_rhino.rs.ShowGroup(thrust_vertices_free)
    compas_rhino.rs.ShowGroup(thrust_vertices_anchor)
    # compas_rhino.rs.ShowObjects(thrust.guid_vertex.keys())

    compas_rhino.rs.Redraw()

    # selection options
    options = ["Continuous", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        ui.scene.update()
        return

    if option == "Continuous":
        edges = thrust.select_edges()
        vertices = list(set(flatten([thrust.diagram.edge_loop_vertices(edge) for edge in edges])))

    elif option == "Manual":
        vertices = thrust.select_vertices()

    thrust_name = thrust.name

    if vertices:
        thrust.select_vertex_points(vertices)

        public = [name for name in form.diagram.default_vertex_attributes if not name.startswith("_")]
        if form.modify_vertices(vertices, names=public):
            thrust.diagram.data = form.diagram.data
            thrust.name = thrust_name
            thrust.is_valid = False

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
