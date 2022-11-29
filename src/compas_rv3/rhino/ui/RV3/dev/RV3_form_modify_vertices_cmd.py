from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten

# from compas_rv3.rhino import ModifyAttributesForm


__commandname__ = "RV3_form_modify_vertices"


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
    options = ["All", "AllBoundaries", "ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)

    if not option:
        scene.update()
        return

    if option == "All":
        keys = list(form.datastructure.vertices())

    elif option == "AllBoundaries":
        keys = list(
            set(
                flatten(
                    [
                        form.datastructure.face_vertices(face)
                        for face in form.datastructure.faces()
                        if form.datastructure.is_face_on_boundary(face)
                    ]
                )
            )
        )

    elif option == "ByContinuousEdges":
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
        # current = scene.settings['RV2']['show.angles']
        # scene.settings['RV2']['show.angles'] = False
        # scene.update()

        # ModifyAttributesForm.from_sceneNode(form, 'vertices', keys)

        # scene.settings['RV2']['show.angles'] = current
        # if thrust:
        #     thrust.settings['_is.valid'] = False
        # scene.update()
        public = [
            name
            for name in form.datastructure.default_vertex_attributes.keys()
            if not name.startswith("_")
        ]
        if form.update_vertices_attributes(keys, names=public):
            if thrust:
                thrust.settings["_is.valid"] = False

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
