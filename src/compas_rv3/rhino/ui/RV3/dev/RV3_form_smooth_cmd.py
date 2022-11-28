from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.utilities import flatten


__commandname__ = "RV3_form_smooth"


def RunCommand(is_interactive):
    scene = get_scene()
    if not scene:
        return

    proxy = get_proxy()
    if not proxy:
        return

    form = scene.get("form")[0]
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    thrust = scene.get("thrust")[0]

    anchors = list(form.datastructure.vertices_where({"is_anchor": True}))
    fixed = list(form.datastructure.vertices_where({"is_fixed": True}))
    fixed = anchors + fixed

    options = ["True", "False"]
    option = compas_rhino.rs.GetString(
        "Press Enter to smooth or ESC to exit. Keep all boundaries fixed?",
        options[0],
        options,
    )

    if option is None:
        print("Form smoothing aborted!")
        return

    if option == "True":
        fixed += list(flatten(form.datastructure.vertices_on_boundaries()))
        fixed += list(
            flatten(
                [
                    form.datastructure.face_vertices(face)
                    for face in form.datastructure.faces_where({"_is_loaded": False})
                ]
            )
        )

    fixed = list(set(fixed))

    form.datastructure.smooth_area(fixed=fixed)

    if thrust:
        thrust.settings["_is.valid"] = False

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
