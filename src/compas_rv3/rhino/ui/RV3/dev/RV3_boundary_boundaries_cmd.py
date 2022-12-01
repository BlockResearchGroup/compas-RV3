from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from functools import partial

from itertools import groupby

import compas_rhino

from compas.geometry import centroid_points
from compas.geometry import distance_point_point_xy
from compas.geometry import intersection_line_line_xy
from compas.geometry import midpoint_point_point_xy
from compas.utilities import pairwise

from compas_ui.ui import UI


__commandname__ = "RV3_boundary_boundaries"


def split_boundary(pattern):
    boundaries = pattern.vertices_on_boundaries()
    exterior = boundaries[0]
    opening = []
    openings = [opening]
    for vertex in exterior:
        opening.append(vertex)
        if pattern.vertex_attribute(vertex, "is_anchor"):
            opening = [vertex]
            openings.append(opening)
    openings[-1] += openings[0]
    del openings[0]
    openings[:] = [opening for opening in openings if len(opening) > 2]
    return [[v[0] for v in groupby(opening)] for opening in openings]


def relax_pattern(pattern, relax):
    key_index = pattern.key_index()
    xyz = pattern.vertices_attributes("xyz")
    loads = [[0.0, 0.0, 0.0] for _ in xyz]
    anchors = [key_index[key] for key in pattern.vertices_where({"is_anchor": True})]
    fixed = [key_index[key] for key in pattern.vertices_where({"is_fixed": True})]
    fixed = list(set(anchors + fixed))
    edges = [(key_index[u], key_index[v]) for u, v in pattern.edges()]
    q = list(pattern.edges_attribute("q"))
    xyz, q, f, l, r = relax(xyz, edges, fixed, q, loads)
    for key in pattern.vertices():
        index = key_index[key]
        pattern.vertex_attributes(key, "xyz", xyz[index])


def compute_sag(pattern, opening):
    u, v = opening[0]
    if pattern.vertex_attribute(u, "is_fixed"):
        a = pattern.vertex_attributes(u, "xyz")
        aa = pattern.vertex_attributes(v, "xyz")
    else:
        a = pattern.vertex_attributes(v, "xyz")
        aa = pattern.vertex_attributes(u, "xyz")
    u, v = opening[-1]
    if pattern.vertex_attribute(u, "is_fixed"):
        b = pattern.vertex_attributes(u, "xyz")
        bb = pattern.vertex_attributes(v, "xyz")
    else:
        b = pattern.vertex_attributes(v, "xyz")
        bb = pattern.vertex_attributes(u, "xyz")
    span = distance_point_point_xy(a, b)
    apex = intersection_line_line_xy((a, aa), (b, bb))
    if apex is None:
        rise = 0.0
    else:
        midspan = midpoint_point_point_xy(a, b)
        rise = 0.5 * distance_point_point_xy(midspan, apex)
    sag = rise / span
    return sag


def _draw_labels(pattern, openings):
    labels = []
    for i, opening in enumerate(openings):
        points = pattern.mesh.vertices_attributes("xyz", keys=opening)
        centroid = centroid_points(points)
        labels.append({"pos": centroid, "text": str(i)})
    return compas_rhino.draw_labels(labels, layer=pattern.settings["layer"], clear=False, redraw=True)


# ==============================================================================
# Command
# ==============================================================================


TOL2 = 0.001**2


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    relax = ui.proxy.function("compas.numerical.fd_numpy")

    pattern = ui.scene.active_object.get_child_by_name("Pattern")
    if not pattern:
        compas_rhino.display_message("No pattern found in the active group.")
        return

    # split the exterior boundary
    openings = split_boundary(pattern.mesh)

    # make a label drawing function
    draw_labels = partial(_draw_labels, pattern, openings)

    # draw a label per opening
    guids = draw_labels()

    # convert the list of vertices to a list of segments
    openings = [list(pairwise(opening)) for opening in openings]

    # compute current opening sags
    targets = []
    for opening in openings:
        sag = compute_sag(pattern.mesh, opening)
        if sag < 0.05:
            sag = 0.05
        targets.append(sag)

    # compute current opening Qs
    Q = []
    for opening in openings:
        q = pattern.mesh.edges_attribute("q", keys=opening)
        q = sum(q) / len(q)
        Q.append(q)
        pattern.mesh.edges_attribute("q", q, keys=opening)

    # relax the pattern
    relax_pattern(pattern.mesh, relax)

    # update Qs to match target sag
    count = 0
    while True and count < 10:
        count += 1
        sags = [compute_sag(pattern.mesh, opening) for opening in openings]
        if all((sag - target) ** 2 < TOL2 for sag, target in zip(sags, targets)):
            break
        for i in range(len(openings)):
            sag = sags[i]
            target = targets[i]
            q = Q[i]
            q = sag / target * q
            Q[i] = q
            opening = openings[i]
            pattern.mesh.edges_attribute("q", Q[i], keys=opening)
        relax_pattern(pattern.mesh, relax)

    if count == 10:
        print("did not converge after 10 iterations")
    else:
        print("converged after %s iterations" % count)

    compas_rhino.delete_objects(guids, purge=True)
    ui.scene.update()
    guids = draw_labels()

    # allow user to select label
    # and specify a target sag
    options1 = ["All"] + ["Boundary{}".format(i) for i, opening in enumerate(openings)]
    options2 = ["Sag_{}".format(i * 5) for i in range(1, 11)]

    while True:
        option1 = compas_rhino.rs.GetString("Select boundary:", strings=options1)

        if not option1:
            break

        if option1 == "All":
            N = [i for i, opening in enumerate(openings)]

        else:
            N = [int(option1[8:])]

        while True:
            option2 = compas_rhino.rs.GetString("Select sag/span percentage:", strings=options2)

            if not option2:
                break

            for boundary in N:

                targets[boundary] = float(option2[4:]) / 100

                count = 0

                while True and count < 10:
                    count += 1
                    sags = [compute_sag(pattern.mesh, opening) for opening in openings]

                    if all((sag - target) ** 2 < TOL2 for sag, target in zip(sags, targets)):
                        break

                    for i in range(len(openings)):
                        sag = sags[i]
                        target = targets[i]
                        q = Q[i]
                        q = sag / target * q
                        Q[i] = q
                        opening = openings[i]
                        pattern.mesh.edges_attribute("q", Q[i], keys=opening)
                    relax_pattern(pattern.mesh, relax)

                if count == 10:
                    print("did not converge after 10 iterations")
                else:
                    print("converged after %s iterations" % count)

            compas_rhino.delete_objects(guids, purge=True)
            ui.scene.update()
            guids = draw_labels()

            break

    compas_rhino.delete_objects(guids, purge=True)
    ui.scene.update()
    ui.record()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    RunCommand(True)
