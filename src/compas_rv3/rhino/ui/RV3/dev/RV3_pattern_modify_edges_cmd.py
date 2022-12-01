from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI


__commandname__ = "RV3_pattern_modify_edges"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = ui.scene.active_object.get_child_by_name("Pattern")
    if not pattern:
        compas_rhino.display_message("No Pattern found in the active group.")
        return

    options = ["All", "Continuous", "Parallel", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type", strings=options)

    if not option:
        return

    if option == "All":
        edges = list(pattern.mesh.edges())

    elif option == "Continuous":
        temp = pattern.select_edges()
        edges = list(set(flatten([pattern.mesh.edge_loop(edge) for edge in temp])))

    elif option == "Parallel":
        temp = pattern.select_edges()
        edges = list(set(flatten([pattern.mesh.edge_strip(edge) for edge in temp])))

    elif option == "Manual":
        edges = pattern.select_edges()

    if edges:
        pattern.select_edge_lines(edges)

        public = [name for name in pattern.mesh.default_edge_attributes if not name.startswith("_")]
        if pattern.modify_edges(edges, names=public):
            ui.scene.update()
            ui.record()


if __name__ == "__main__":
    RunCommand(True)
