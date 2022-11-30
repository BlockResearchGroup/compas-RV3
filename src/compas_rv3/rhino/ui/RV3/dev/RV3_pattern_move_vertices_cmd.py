from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

__commandname__ = "RV3_pattern_move_vertices"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = get_object_by_name("Pattern")

    options = ["ByContinuousEdges", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type.", strings=options)
    if not option:
        return

    if option == "ByContinuousEdges":
        temp = pattern.select_edges()
        keys = list(set(flatten([pattern.datastructure.vertices_on_edge_loop(key) for key in temp])))

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
    #         for key in pattern.datastructure.vertices():
    #             if if_constraints(pattern.datastructure, key, guid):
    #                 keys.append(key)

    #     keys = list(set(keys))

    #     compas_rhino.rs.HideObjects(guids)
    #     pattern.settings['color.edges'] = current

    elif option == "Manual":
        keys = pattern.select_vertices()

    if keys:
        compas_rhino.rs.UnselectAllObjects()
        select_vertices(pattern, keys)

        if pattern.move_vertices(keys):
            ui.scene.update()
            ui.record()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
