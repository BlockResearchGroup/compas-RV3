from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.geometry import RhinoMesh
from compas_ui.ui import UI
from compas_ui.objects import Group
from compas_rv3.datastructures import Pattern


__commandname__ = "RV3_pattern_from_mesh"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    guid = compas_rhino.select_mesh()
    if not guid:
        return

    pattern = RhinoMesh.from_guid(guid).to_compas(cls=Pattern)

    compas_rhino.rs.HideObject(guid)

    group = ui.scene.add(Group(), name="RV3")
    group.add(pattern, name="Pattern")
    ui.scene.active_object = group
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
