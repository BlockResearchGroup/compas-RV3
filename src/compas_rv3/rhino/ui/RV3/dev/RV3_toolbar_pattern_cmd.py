from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

import RV3_pattern_from_lines_cmd
import RV3_pattern_from_mesh_cmd
import RV3_pattern_from_triangulation_cmd

# import RV3_pattern_from_surfaces_cmd


__commandname__ = "RV3_toolbar_pattern"


def RunCommand(is_interactive):

    options = ["FromLines", "FromMesh", "FromSurfaces", "FromTriangulation"]
    option = compas_rhino.rs.GetString("Create Pattern:", strings=options)

    if not option:
        return

    if option == "FromLines":
        RV3_pattern_from_lines_cmd.RunCommand(True)

    elif option == "FromMesh":
        RV3_pattern_from_mesh_cmd.RunCommand(True)

    # elif option == "FromSurfaces":
    #     RV3_pattern_from_surfaces_cmd.RunCommand(True)

    elif option == "FromTriangulation":
        RV3_pattern_from_triangulation_cmd.RunCommand(True)


if __name__ == "__main__":
    RunCommand(True)
