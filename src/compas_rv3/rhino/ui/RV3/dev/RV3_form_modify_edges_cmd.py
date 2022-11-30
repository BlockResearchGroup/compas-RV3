from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name
# from compas_rv3.rhino import ModifyAttributesForm


__commandname__ = "RV3_form_modify_edges"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    form = get_object_by_name("FormDiagram")
    thrust = get_object_by_name("ThrustDiagram")

    options = ["All", "Continuous", "Parallel", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)

    if not option:
        return

    if option == "All":
        keys = list(form.datastructure.edges())

    elif option == "Continuous":
        temp = form.select_edges()
        keys = list(set(flatten([form.datastructure.edge_loop(key) for key in temp])))

    elif option == "Parallel":
        temp = form.select_edges()
        keys = list(set(flatten([form.datastructure.edge_strip(key) for key in temp])))

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

    #     def if_constraints(datastructure, key, guid):
    #         constraints = datastructure.vertex_attribute(key, 'constraints')
    #         if constraints:
    #             if str(guid) in constraints:
    #                 return True
    #         return False

    #     keys = []
    #     for guid in constraints:
    #         for (u, v) in form.datastructure.edges():
    #             if if_constraints(form.datastructure, u, guid) and if_constraints(form.datastructure, v, guid):
    #                 keys.append((u, v))

    #     compas_rhino.rs.HideObjects(guids)
    #     form.settings['color.edges'] = current

    elif option == "Manual":
        keys = form.select_edges()

    if keys:
        # current = scene.settings['RV2']['show.angles']
        # scene.settings['RV2']['show.angles'] = False
        # scene.update()

        # ModifyAttributesForm.from_sceneNode(form, 'edges', keys)

        # scene.settings['RV2']['show.angles'] = current
        # if thrust:
        #     thrust.settings['_is.valid'] = False
        # scene.update()
        public = [
            name
            for name in form.datastructure.default_edge_attributes.keys()
            if not name.startswith("_")
        ]
        if form.update_edges_attributes(keys, names=public):
            if thrust:
                thrust.settings["_is.valid"] = False

    ui.scene.update()
    ui.record()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
