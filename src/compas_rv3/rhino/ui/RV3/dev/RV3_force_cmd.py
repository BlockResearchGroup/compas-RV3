from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Translation

from compas_rv3.datastructures import ForceDiagram


__commandname__ = "RV3_force"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    form = scene.get("form")[0]
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    force = scene.get("force")[0]
    if force:
        # recreating the force diagram does not work
        return

    force = ForceDiagram.from_formdiagram(form.datastructure)
    force.default_edge_attributes.update({"lmin": 0.1})

    bbox_form = form.datastructure.bounding_box_xy()
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

    scene.add(force, name="force")

    scene.update()

    print("ForceDiagram object successfully created.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
