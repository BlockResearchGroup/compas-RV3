from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import subtract_vectors
from compas.geometry import length_vector
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name


__commandname__ = "RV3_tna_vertical"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    vertical = ui.proxy.function("compas_tna.equilibrium.vertical_from_zmax_proxy")

    form = get_object_by_name("FormDiagram")
    force = get_object_by_name("ForceDiagram")
    thrust = get_object_by_name("ThrustDiagram")

    bbox = form.diagram.bounding_box_xy()
    diagonal = length_vector(subtract_vectors(bbox[2], bbox[0]))

    zmax = ui.scene.settings["tna.vertical.zmax"]
    kmax = ui.scene.settings["tna.vertical.kmax"]

    options = ["TargetHeight"]

    while True:
        option = compas_rhino.rs.GetString("Press Enter to run or ESC to exit.", strings=options)

        if option is None:
            print("Vetical equilibrium aborted!")
            return

        if not option:
            break

        if option == "TargetHeight":
            new_zmax = compas_rhino.rs.GetReal("Enter target height of the ThrustDiagram", zmax, 0.0, 1.0 * diagonal)
            if new_zmax or new_zmax is not None:
                zmax = new_zmax

    ui.scene.settings["tna.vertical.zmax"] = zmax

    result = vertical(form.diagram.data, zmax, kmax=kmax)

    if not result:
        compas_rhino.display_message("Vertical equilibrium failed!")
        return

    formdata, scale = result

    # store in advance such that it can be reset
    thrust_name = thrust.name

    force.diagram.attributes["scale"] = scale
    form.diagram.data = formdata
    thrust.diagram.data = formdata

    # the name of the thrust diagram is stored in the attribute dict of the mesh
    # therefore the name must be reset explicitly
    thrust.name = thrust_name

    form.diagram.dual = force.diagram
    force.diagram.primal = form.diagram
    thrust.diagram.dual = force.diagram

    thrust.settings["_is.valid"] = True

    compas_rhino.display_message("Vertical equilibrium found!\nThrustDiagram object successfully created with target height of {}.".format(zmax))

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
