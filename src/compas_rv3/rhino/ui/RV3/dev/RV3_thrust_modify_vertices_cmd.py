from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino


__commandname__ = "RV3_thrust_modify_vertices"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    form = scene.get("form")[0]
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    thrust = scene.get("thrust")[0]
    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    # hide the form vertices
    form_vertices = "{}::vertices".format(form.settings["layer"])
    compas_rhino.rs.HideGroup(form_vertices)

    # show the thrust vertices
    thrust_vertices_free = "{}::vertices_free".format(thrust.settings["layer"])
    thrust_vertices_anchor = "{}::vertices_anchor".format(thrust.settings["layer"])
    compas_rhino.rs.ShowGroup(thrust_vertices_free)
    compas_rhino.rs.ShowGroup(thrust_vertices_anchor)
    compas_rhino.rs.Redraw()

    # selection options
    options = ["Continuous", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        scene.update()
        return

    if option == "Continuous":
        temp = thrust.select_edges()
        keys = list(
            set(
                flatten(
                    [thrust.datastructure.vertices_on_edge_loop(key) for key in temp]
                )
            )
        )

    elif option == "Manual":
        keys = thrust.select_vertices()

    thrust_name = thrust.name

    if keys:
        public = [
            name
            for name in form.datastructure.default_vertex_attributes.keys()
            if not name.startswith("_")
        ]
        if form.update_vertices_attributes(keys, names=public):
            thrust.datastructure.data = form.datastructure.data
            thrust.name = thrust_name
            thrust.settings["_is.valid"] = False

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
