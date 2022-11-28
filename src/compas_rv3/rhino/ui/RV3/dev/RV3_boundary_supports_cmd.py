from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import flatten

import compas_rhino


__commandname__ = "RV3_boundary_supports"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    pattern = scene.get("pattern")[0]
    if not pattern:
        print("There is no Pattern in the scene.")
        return

    # mark all fixed vertices as anchors
    # mark all leaves as anchors

    fixed = list(pattern.datastructure.vertices_where({"is_fixed": True}))
    leaves = []
    for vertex in pattern.datastructure.vertices():
        nbrs = pattern.datastructure.vertex_neighbors(vertex)
        count = 0
        for nbr in nbrs:
            if pattern.datastructure.edge_attribute((vertex, nbr), "_is_edge"):
                count += 1
        if count == 1:
            leaves.append(vertex)

    anchors = list(set(fixed) | set(leaves))
    if anchors:
        pattern.datastructure.vertices_attribute("is_anchor", True, keys=anchors)
        print(
            "Fixed vertices of the pattern have automatically been defined as supports."
        )
        scene.update()

    # manually Select or Unselect
    # should this not be included in the while loop?

    options = ["Select", "Unselect"]
    option1 = compas_rhino.rs.GetString(
        "Select or unselect vertices as supports:", strings=options
    )

    if not option1:
        return

    options = ["AllBoundaryVertices", "Corners", "ByContinuousEdges", "Manual"]

    while True:
        option2 = compas_rhino.rs.GetString("Selection mode:", strings=options)

        if not option2:
            return

        if option2 == "AllBoundaryVertices":
            keys = list(set(flatten(pattern.datastructure.vertices_on_boundaries())))

        elif option2 == "Corners":
            angle = compas_rhino.rs.GetInteger(
                "Angle tolerance for non-quad face corners:", 170, 1, 180
            )
            keys = pattern.datastructure.corner_vertices(tol=angle)

        elif option2 == "ByContinuousEdges":
            edges = pattern.select_edges()
            keys = list(
                set(
                    flatten(
                        [
                            pattern.datastructure.vertices_on_edge_loop(edge)
                            for edge in edges
                        ]
                    )
                )
            )

        # elif option2 == "ByConstraint":

        #     def predicate(constraints, key, attr):
        #         if not constraints:
        #             return False
        #         if not attr['constraints']:
        #             return False
        #         return any(constraint in attr['constraints'] for constraint in constraints)

        #     temp = pattern.select_vertices()
        #     keys = list(set(flatten(
        #         [pattern.datastructure.vertices_where_predicate(
        #             partial(predicate, pattern.datastructure.vertex_attribute(vertex, 'constraints'))) for vertex in temp])))

        elif option2 == "Manual":
            keys = pattern.select_vertices()

        if keys:
            if option1 == "Select":
                pattern.datastructure.vertices_attribute("is_anchor", True, keys=keys)
            else:
                pattern.datastructure.vertices_attribute("is_anchor", False, keys=keys)

        scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
