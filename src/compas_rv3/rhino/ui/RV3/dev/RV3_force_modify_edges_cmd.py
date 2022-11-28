from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino

# from compas_rv2.rhino import ModifyAttributesForm


__commandname__ = "RV3_force_modify_edges"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    force = scene.get("force")[0]
    if not force:
        print("There is no ForceDiagram in the scene.")
        return

    thrust = scene.get("thrust")[0]

    options = ["All", "Continuous", "Parallel", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "All":
        keys = list(force.datastructure.edges())

    elif option == "Continuous":
        edges = force.select_edges()
        keys = list(
            set(flatten([force.datastructure.edge_loop(edge) for edge in edges]))
        )

    elif option == "Parallel":
        temp = force.select_edges()
        keys = list(set(flatten([force.datastructure.edge_strip(key) for key in temp])))

    # elif option == "ByConstraints":
    #     # find the formdiagram edge on the constraints
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

    #     def if_constraints(datastructure, key, guid):
    #         constraints = datastructure.vertex_attribute(key, 'constraints')
    #         if constraints:
    #             if str(guid) in constraints:
    #                 return True
    #         return False

    #     keys_form = []
    #     for guid in constraints:
    #         for (u, v) in form.datastructure.edges():
    #             if if_constraints(form.datastructure, u, guid) and if_constraints(form.datastructure, v, guid):
    #                 keys_form.append((u, v))

    #     compas_rhino.rs.HideObjects(guids)
    #     form.settings['color.edges'] = current

    #     # find corrresponding edges on the force
    #     keys = []
    #     for (u, v) in force.datastructure.edges():
    #         uf, vf = force.datastructure.primal_edge((u, v))
    #         if ((uf, vf) in keys_form) or ((vf, uf) in keys_form):
    #             keys.append((u, v))

    elif option == "Manual":
        keys = force.select_edges()

    if keys:
        # current = scene.settings['RV2']['show.angles']
        # scene.settings['RV2']['show.angles'] = False
        # scene.update()

        # ModifyAttributesForm.from_sceneNode(force, 'edges', keys)

        # scene.settings['RV2']['show.angles'] = current
        # if thrust:
        #     thrust.settings['_is.valid'] = False
        # scene.update()
        public = [
            name
            for name in force.datastructure.default_edge_attributes.keys()
            if not name.startswith("_")
        ]
        if force.update_edges_attributes(keys, names=public):
            if thrust:
                thrust.settings["_is.valid"] = False

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
