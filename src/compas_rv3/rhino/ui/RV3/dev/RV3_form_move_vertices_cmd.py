from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI


__commandname__ = "RV3_form_move_vertices"


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

    # show the form vertices
    form_vertices = "{}::vertices".format(form.settings["layer"])
    compas_rhino.rs.ShowGroup(form_vertices)
    # compas_rhino.rs.ShowObjects(form.guid_vertex.keys())

    if thrust:
        # hide the thrust vertices
        thrust_vertices_free = "{}::vertices_free".format(thrust.settings["layer"])
        thrust_vertices_anchor = "{}::vertices_anchor".format(thrust.settings["layer"])
        compas_rhino.rs.HideGroup(thrust_vertices_free)
        compas_rhino.rs.HideGroup(thrust_vertices_anchor)
        # compas_rhino.rs.HideObjects(thrust.guid_vertex.keys())

    compas_rhino.rs.Redraw()

    # selection options
    options = ["ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        ui.scene.update()
        return

    if option == "ByContinuousEdges":
        edges = form.select_edges()
        vertices = list(set(flatten([form.diagram.edge_loop_vertices(edge) for edge in edges])))

    elif option == "Manual":
        vertices = form.select_vertices()

    if vertices:
        if form.move_vertices_direction(vertices, "xy"):
            if form.diagram.dual:
                form.diagram.dual.update_angle_deviations()
            if thrust:
                thrust.is_valid = False

    # the scene needs to be updated
    # even if the vertices where not modified
    # to reset group visibility to the configuration of settings
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
