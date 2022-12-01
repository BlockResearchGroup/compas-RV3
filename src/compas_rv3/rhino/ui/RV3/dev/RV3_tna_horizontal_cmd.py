from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.geometry import Translation
from compas_tna.equilibrium import horizontal_nodal
from compas_rv3.rhino.conduits import HorizontalConduit
from compas_ui.ui import UI


__commandname__ = "RV3_tna_horizontal"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    def redraw(k, xy, edges):
        if k % conduit.refreshrate:
            return
        print(k)
        conduit.lines = [[[xy[i][1], -xy[i][0]], [xy[j][1], -xy[j][0]]] for i, j in edges]
        conduit.redraw()

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

    kmax = ui.registry["RV3"]["tna.horizontal.kmax"]
    alpha = ui.registry["RV3"]["tna.horizontal.alpha"]
    refresh = ui.registry["RV3"]["tna.horizontal.refreshrate"]

    options = ["Alpha", "Iterations", "RefreshRate"]

    while True:
        option = compas_rhino.rs.GetString("Press Enter to run or ESC to exit.", strings=options)

        if option is None:
            compas_rhino.display_message("Horizontal equilibrium aborted!")
            return

        if not option:
            break

        if option == "Alpha":
            alpha_options = ["form{}".format(int(i * 10)) for i in range(11)]
            alpha_default = 0
            for i in range(11):
                if alpha == i * 10:
                    alpha_default = i
                    break

            temp = compas_rhino.rs.GetString("Select parallelisation weight", alpha_options[alpha_default], alpha_options)
            if not temp:
                alpha = 100
            else:
                alpha = int(temp[4:])

        elif option == "Iterations":
            new_kmax = compas_rhino.rs.GetInteger("Enter number of iterations", kmax, 1, 10000)
            if new_kmax or new_kmax is not None:
                kmax = new_kmax

        elif option == "RefreshRate":
            new_refresh = compas_rhino.rs.GetInteger("Refresh rate for dynamic visualisation", refresh, 0, 1000)
            if new_refresh or new_refresh is not None:
                refresh = new_refresh

    if refresh > kmax:
        refresh = 0

    ui.registry["RV3"]["tna.horizontal.kmax"] = kmax
    ui.registry["RV3"]["tna.horizontal.alpha"] = alpha
    ui.registry["RV3"]["tna.horizontal.refreshrate"] = refresh

    force.artist.clear()

    if refresh > 0:
        conduit = HorizontalConduit([], refreshrate=refresh)
        with conduit.enabled():
            horizontal_nodal(form.diagram, force.diagram, kmax=kmax, alpha=alpha, callback=redraw)
    else:
        horizontal_nodal(form.diagram, force.diagram, kmax=kmax, alpha=alpha)

    bbox_form = form.diagram.bounding_box_xy()
    bbox_force = force.diagram.bounding_box_xy()
    xmin_form, xmax_form = bbox_form[0][0], bbox_form[1][0]
    xmin_force, _ = bbox_force[0][0], bbox_force[1][0]
    ymin_form, ymax_form = bbox_form[0][1], bbox_form[3][1]
    ymin_force, ymax_force = bbox_force[0][1], bbox_force[3][1]
    y_form = ymin_form + 0.5 * (ymax_form - ymin_form)
    y_force = ymin_force + 0.5 * (ymax_force - ymin_force)
    dx = 1.3 * (xmax_form - xmin_form) + (xmin_form - xmin_force)
    dy = y_form - y_force

    force.diagram.transform(Translation.from_vector([dx, dy, 0]))
    force.diagram.update_angle_deviations()

    thrust.is_valid = False

    max_angle = max(form.diagram.edges_attribute("_a"))
    tol = ui.registry["RV3"]["tol.angles"]

    if max_angle < tol:
        print("Horizontal equilibrium found!\nMaximum angle deviation: {}".format(max_angle))
    else:
        compas_rhino.display_message("Horizontal equilibrium NOT found! Consider running more iterations.\nMaximum angle deviation: {}".format(max_angle))

    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
