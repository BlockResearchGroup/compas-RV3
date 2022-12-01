from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import subtract_vectors
from compas.geometry import length_vector
from compas_ui.ui import UI


__commandname__ = "RV3_tna_vertical"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    vertical = ui.proxy.function("compas_tna.equilibrium.vertical_from_zmax")

    form = ui.scene.active_object.get_child_by_name("FormDiagram")
    if not form:
        compas_rhino.display_message("No FormDiagram found in the active group.")
        return

    force = ui.scene.active_object.get_child_by_name("ForceDiagram")
    if not force:
        compas_rhino.display_message("No ForceDiagram found in the active group.")
        return

    thrust = ui.scene.active_object.get_child_by_name("ThrustDiagram")
    if not thrust:
        compas_rhino.display_message("No ThrustDiagram found in the active group.")
        return

    bbox = form.diagram.bounding_box_xy()
    diagonal = length_vector(subtract_vectors(bbox[2], bbox[0]))

    zmax = ui.registry["RV3"]["tna.vertical.zmax"]
    kmax = ui.registry["RV3"]["tna.vertical.kmax"]

    new_zmax = compas_rhino.rs.GetReal("Enter target height of the ThrustDiagram", zmax, 0.0, 1.0 * diagonal)
    if new_zmax:
        zmax = new_zmax

    ui.registry["RV3"]["tna.vertical.zmax"] = zmax

    result = vertical(form.diagram, zmax, kmax=kmax)

    if not result:
        compas_rhino.display_message("Vertical equilibrium failed!")
        return

    formdiagram, scale = result

    # store in advance such that it can be reset
    thrust_name = thrust.name

    force.diagram.attributes["scale"] = scale
    form.diagram.data = formdiagram.data
    thrust.diagram.data = formdiagram.data

    # the name of the thrust diagram is stored in the attribute dict of the mesh
    # therefore the name must be reset explicitly
    thrust.name = thrust_name

    form.diagram.dual = force.diagram
    force.diagram.primal = form.diagram
    thrust.diagram.dual = force.diagram

    thrust.is_valid = True

    print("Vertical equilibrium found!\nThrustDiagram object successfully created with target height of {}.".format(zmax))

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
