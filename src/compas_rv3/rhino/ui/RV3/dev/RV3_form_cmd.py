from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas.geometry import subtract_vectors
from compas.geometry import length_vector
from compas.geometry import scale_vector
from compas.geometry import sum_vectors

from compas_rv3.datastructures import ThrustDiagram
from compas_rv3.datastructures import FormDiagram

from compas_ui.ui import UI


__commandname__ = "RV3_form"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    pattern = ui.scene.active_object.get_child_by_name("Pattern")
    if not pattern:
        compas_rhino.display_message("No Pattern found in the active group.")
        return

    if not list(pattern.mesh.vertices_where(is_anchor=True)):
        compas_rhino.display_message("Pattern has no anchor vertices! Please define anchor (support) vertices.")
        return

    form = FormDiagram.from_pattern(pattern.mesh)
    form.vertices_attribute("is_fixed", False)

    normals = [form.face_normal(face) for face in form.faces_where(_is_loaded=True)]
    scale = 1 / len(normals)
    normal = scale_vector(sum_vectors(normals), scale)
    if normal[2] < 0:
        form.flip_cycles()

    fixed = list(pattern.mesh.vertices_where(is_fixed=True))

    if fixed:
        for vertex in fixed:
            if form.has_vertex(vertex):
                form.vertex_attribute(vertex, "is_anchor", True)

    thrust = form.copy(cls=ThrustDiagram)
    bbox_form = form.bounding_box_xy()
    diagonal = length_vector(subtract_vectors(bbox_form[2], bbox_form[0]))
    zmax = 0.25 * diagonal

    ui.registry["RV3"]["tna.vertical.zmax"] = round(zmax, 1)

    group = ui.scene.active_object
    group.clear()
    group.add(form, name="FormDiagram")
    group.add(thrust, name="ThrustDiagram")
    ui.scene.active_object = group

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
