from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten


__commandname__ = "RV3_form_move_vertices"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    form = scene.get("form")[0]
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    thrust = scene.get("thrust")[0]

    # show the form vertices
    form_vertices = "{}::vertices".format(form.settings["layer"])
    compas_rhino.rs.ShowGroup(form_vertices)

    if thrust:
        # hide the thrust vertices
        thrust_vertices_free = "{}::vertices_free".format(thrust.settings["layer"])
        thrust_vertices_anchor = "{}::vertices_anchor".format(thrust.settings["layer"])
        compas_rhino.rs.HideGroup(thrust_vertices_free)
        compas_rhino.rs.HideGroup(thrust_vertices_anchor)

    compas_rhino.rs.Redraw()

    # selection options
    options = ["ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        scene.update()
        return

    if option == "ByContinuousEdges":
        temp = form.select_edges()
        keys = list(
            set(
                flatten([form.datastructure.vertices_on_edge_loop(key) for key in temp])
            )
        )

    # elif option == "ByConstraints":
    #     guids = form.datastructure.vertices_attribute('constraints')
    #     guids = list(set(list(flatten(list(filter(None, guids))))))

    #     if not guids:
    #         print('there are no constraints in this form')
    #         return

    #     current = form.settings['color.edges']
    #     form.settings['color.edges'] = [120, 120, 120]
    #     scene.update()

    #     compas_rhino.rs.ShowObjects(guids)

    #     def custom_filter(rhino_object, geometry, component_index):
    #         if str(rhino_object.Id) in guids:
    #             return True
    #         return False

    #     constraints = compas_rhino.rs.GetObjects('select constraints', custom_filter=custom_filter)

    #     if not constraints:
    #         return

    #     keys = []
    #     for guid in constraints:
    #         for key, attr in form.datastructure.vertices(data=True):
    #             if attr['constraints']:
    #                 if str(guid) in attr['constraints']:
    #                     keys.append(key)
    #     keys = list(set(keys))

    #     compas_rhino.rs.HideObjects(guids)
    #     form.settings['color.edges'] = current

    elif option == "Manual":
        keys = form.select_vertices()

    if keys:
        if form.move_vertices_horizontal(keys):
            if form.datastructure.dual:
                form.datastructure.dual.update_angle_deviations()
            if thrust:
                thrust.settings["_is.valid"] = False

    # the scene needs to be updated
    # even if the vertices where not modified
    # to reset group visibility to the configuration of settings
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
