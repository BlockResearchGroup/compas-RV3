from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import subtract_vectors
from compas.geometry import length_vector
from compas.geometry import scale_vector
from compas.geometry import sum_vectors

from compas_rv3.datastructures import ThrustDiagram
from compas_rv3.datastructures import FormDiagram

from compas_ui.ui import UI
from compas_rv3.rhino.helpers import get_object_by_name

__commandname__ = "RV3_form"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = get_object_by_name("Pattern")

    if not list(pattern.datastructure.vertices_where({"is_anchor": True})):
        print("Pattern has no anchor vertices! Please define anchor (support) vertices.")
        return

    form = FormDiagram.from_pattern(pattern.datastructure)
    form.vertices_attribute("is_fixed", False)

    normals = [form.face_normal(face) for face in form.faces_where({"_is_loaded": True})]
    scale = 1 / len(normals)
    normal = scale_vector(sum_vectors(normals), scale)
    if normal[2] < 0:
        form.flip_cycles()

    fixed = list(pattern.datastructure.vertices_where({"is_fixed": True}))

    if fixed:
        for key in fixed:
            if form.has_vertex(key):
                form.vertex_attribute(key, "is_anchor", True)

    thrust = form.copy(cls=ThrustDiagram)
    bbox_form = form.bounding_box_xy()
    diagonal = length_vector(subtract_vectors(bbox_form[2], bbox_form[0]))
    zmax = 0.25 * diagonal

    ui.scene.settings["tna.vertical.zmax"] = round(zmax, 1)
    ui.scene.clear()
    ui.scene.add(form, name="FormDiagram")
    ui.scene.add(thrust, name="ThrustDiagram")
    ui.scene.update()
    ui.record()

    print("FormDiagram object successfully created.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
