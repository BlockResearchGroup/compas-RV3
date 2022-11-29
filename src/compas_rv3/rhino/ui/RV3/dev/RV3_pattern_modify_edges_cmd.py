from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten

# from compas_rv3.rhino import ModifyAttributesForm


__commandname__ = "RV3_pattern_modify_edges"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    options = ["All", "Continuous", "Parallel", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type", strings=options)

    if not option:
        return

    if option == "All":
        keys = keys = list(pattern.datastructure.edges())

    elif option == "Continuous":
        temp = pattern.select_edges()
        keys = list(
            set(flatten([pattern.datastructure.edge_loop(key) for key in temp]))
        )

    elif option == "Parallel":
        temp = pattern.select_edges()
        keys = list(
            set(flatten([pattern.datastructure.edge_strip(key) for key in temp]))
        )

    # elif option == "ByConstraints":
    #     guids = pattern.datastructure.vertices_attribute('constraints')
    #     guids = list(set(list(flatten(list(filter(None, guids))))))

    #     if not guids:
    #         print('there are no constraints in this pattern')
    #         return

    #     current = pattern.settings['color.edges']
    #     pattern.settings['color.edges'] = [120, 120, 120]
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
    #         for (u, v) in pattern.datastructure.edges():
    #             if if_constraints(pattern.datastructure, u, guid) and if_constraints(pattern.datastructure, v, guid):
    #                 keys.append((u, v))

    #     compas_rhino.rs.HideObjects(guids)
    #     pattern.settings['color.edges'] = current

    elif option == "Manual":
        keys = pattern.select_edges()

    if keys:
        # ModifyAttributesForm.from_sceneNode(pattern, 'edges', keys)
        # scene.update()
        public = [
            name
            for name in pattern.datastructure.default_edge_attributes.keys()
            if not name.startswith("_")
        ]
        if pattern.update_edges_attributes(keys, names=public):
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
