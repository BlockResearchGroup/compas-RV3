from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Translation
from compas_rv3.datastructures import ForceDiagram
from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name


__commandname__ = "RV3_force"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    form = get_object_by_name("FormDiagram")

    objects = ui.scene.get("ForceDiagram")
    if objects:
        raise RuntimeError("Recreating the force diagram does not work")

    force = ForceDiagram.from_formdiagram(form.diagram)
    force.default_edge_attributes.update({"lmin": 0.1})

    bbox_form = form.diagram.bounding_box_xy()
    bbox_force = force.bounding_box_xy()
    xmin_form, xmax_form = bbox_form[0][0], bbox_form[1][0]
    xmin_force, _ = bbox_force[0][0], bbox_force[1][0]
    ymin_form, ymax_form = bbox_form[0][1], bbox_form[3][1]
    ymin_force, ymax_force = bbox_force[0][1], bbox_force[3][1]
    y_form = ymin_form + 0.5 * (ymax_form - ymin_form)
    y_force = ymin_force + 0.5 * (ymax_force - ymin_force)
    dx = 1.3 * (xmax_form - xmin_form) + (xmin_form - xmin_force)
    dy = y_form - y_force

    force.transform(Translation.from_vector([dx, dy, 0]))
    force.update_angle_deviations()

    ui.scene.add(force, name="ForceDiagram")

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
