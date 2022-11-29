from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoMesh
from compas_rv3.datastructures import Pattern


__commandname__ = "RV3_pattern_from_mesh"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    guid = compas_rhino.select_mesh()
    if not guid:
        return

    pattern = RhinoMesh.from_guid(guid).to_compas(cls=Pattern)

    compas_rhino.rs.HideObject(guid)

    scene.clear()
    scene.add(pattern, name="Pattern")
    scene.update()

    print("Pattern object successfully created. Input mesh has been hidden.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
