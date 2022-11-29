from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten

# from compas_rv3.rhino import ModifyAttributesForm


__commandname__ = "RV3_pattern_modify_vertices"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    options = ["AllBoundaryVertices", "Corners", "ByContinuousEdges", "Manual"]

    option = compas_rhino.rs.GetString("Selection mode:", strings=options)

    if not option:
        return

    if option == "AllBoundaryVertices":
        keys = pattern.datastructure.vertices_on_boundary()

    elif option == "Corners":
        angle = compas_rhino.rs.GetInteger(
            "Angle tolerance for non-quad face corners:", 170, 1, 180
        )
        keys = pattern.datastructure.corner_vertices(tol=angle)

    elif option == "ByContinuousEdges":
        temp = pattern.select_edges()
        keys = list(
            set(
                flatten(
                    [pattern.datastructure.vertices_on_edge_loop(key) for key in temp]
                )
            )
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

    #     keys = []
    #     for guid in constraints:
    #         for key, attr in pattern.datastructure.vertices(data=True):
    #             if attr['constraints']:
    #                 if str(guid) in attr['constraints']:
    #                     keys.append(key)
    #     keys = list(set(keys))

    #     compas_rhino.rs.HideObjects(guids)
    #     pattern.settings['color.edges'] = current

    elif option == "Manual":
        keys = pattern.select_vertices()

    if keys:
        # ModifyAttributesForm.from_sceneNode(pattern, 'vertices', keys)
        # scene.update()
        public = [
            name
            for name in pattern.datastructure.default_vertex_attributes.keys()
            if not name.startswith("_")
        ]
        if pattern.update_vertices_attributes(keys, names=public):
            scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
