from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name


__commandname__ = "RV3_pattern_modify_edges"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = get_object_by_name("Pattern")

    options = ["All", "Continuous", "Parallel", "Manual"]
    option = compas_rhino.rs.GetString("Selection Type", strings=options)

    if not option:
        return

    if option == "All":
        edges = list(pattern.datastructure.edges())

    elif option == "Continuous":
        temp = pattern.select_edges()
        edges = list(set(flatten([pattern.datastructure.edge_loop(edge) for edge in temp])))

    elif option == "Parallel":
        temp = pattern.select_edges()
        edges = list(set(flatten([pattern.datastructure.edge_strip(edge) for edge in temp])))

    elif option == "Manual":
        edges = pattern.select_edges()

    if edges:
        public = [name for name in pattern.datastructure.default_edge_attributes if not name.startswith("_")]
        if pattern.update_edges_attributes(edges, names=public):
            ui.scene.update()
            ui.record()


if __name__ == "__main__":
    RunCommand(True)
