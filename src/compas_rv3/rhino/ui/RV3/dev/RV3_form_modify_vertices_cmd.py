from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI


__commandname__ = "RV3_form_modify_vertices"


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
    options = ["All", "AllBoundaries", "ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)

    if not option:
        ui.scene.update()
        return

    if option == "All":
        vertices = list(form.diagram.vertices())

    elif option == "AllBoundaries":
        vertices = list(set(flatten([form.diagram.face_vertices(face) for face in form.diagram.faces() if form.diagram.is_face_on_boundary(face)])))

    elif option == "ByContinuousEdges":
        edges = form.select_edges()
        vertices = list(set(flatten([form.diagram.edge_loop_vertices(edge) for edge in edges])))

    elif option == "Manual":
        vertices = form.select_vertices()

    if vertices:
        form.select_vertex_points(vertices)

        public = [name for name in form.diagram.default_vertex_attributes if not name.startswith("_")]
        if form.modify_vertices(vertices, names=public):
            if thrust:
                thrust.is_valid = False

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
