from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_ui.ui import UI
from compas_ui.objects import Group

from compas.utilities import geometric_key
from compas_rhino.geometry import RhinoCurve
from compas_rv3.datastructures import Pattern


__commandname__ = "RV3_pattern_from_triangulation"


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    refined_delaunay_mesh = ui.proxy.function("compas_cgal.triangulation.refined_delaunay_mesh")

    boundary_guids = compas_rhino.select_curves("Select outer boundary.")
    if not boundary_guids:
        return
    compas_rhino.rs.UnselectAllObjects()

    hole_guids = compas_rhino.select_curves("Select inner boundaries.")
    compas_rhino.rs.UnselectAllObjects()

    segments_guids = compas_rhino.select_curves("Select constraint curves.")
    compas_rhino.rs.UnselectAllObjects()

    target_length = compas_rhino.rs.GetReal("Specifiy target edge length.", 1.0)
    if not target_length:
        return

    gkey_constraints = {}

    # outer boundary
    boundary = []
    for guid in boundary_guids:
        compas_rhino.rs.EnableRedraw(False)
        segments = compas_rhino.rs.ExplodeCurves(guid)
        for segment in segments:
            curve = RhinoCurve.from_guid(segment).to_compas()
            N = max(int(curve.length() / target_length), 1)
            _, points = curve.divide_by_count(N, return_points=True)
            for point in points:
                gkey = geometric_key(point)
                if gkey not in gkey_constraints:
                    gkey_constraints[gkey] = []
                gkey_constraints[gkey].append(segment)
            boundary.extend(points)
        compas_rhino.rs.HideObjects(segments)
        compas_rhino.rs.EnableRedraw(True)

    # constraint polylines
    polylines = []
    if segments_guids:
        for guid in segments_guids:
            curve = RhinoCurve.from_guid(guid).to_compas()
            N = int(curve.length() / target_length) or 1
            _, points = curve.divide_by_count(N, return_points=True)
            for point in points:
                gkey = geometric_key(point)
                if gkey not in gkey_constraints:
                    gkey_constraints[gkey] = []
                gkey_constraints[gkey].append(guid)
            polylines.append(points)

    # hole polygons
    polygons = []
    if hole_guids:
        for guid in hole_guids:
            curve = RhinoCurve.from_guid(guid).to_compas()
            N = int(curve.length() / target_length) or 1
            _, points = curve.divide_by_count(N, return_points=True)
            for point in points[:-1]:
                gkey = geometric_key(point)
                if gkey not in gkey_constraints:
                    gkey_constraints[gkey] = []
                gkey_constraints[gkey].append(guid)
            polygons.append(points)

    vertices, faces = refined_delaunay_mesh(boundary, curves=polylines, holes=polygons, maxlength=target_length, is_optimized=True)
    vertices[:] = [[float(x), float(y), float(z)] for x, y, z in vertices]

    pattern = Pattern.from_vertices_and_faces(vertices, faces)

    gkey_vertex = {geometric_key(pattern.vertex_coordinates(vertex)): vertex for vertex in pattern.vertices()}

    for gkey in gkey_constraints:
        guids = gkey_constraints[gkey]
        if gkey in gkey_vertex:
            vertex = gkey_vertex[gkey]
            if len(guids) > 1:
                pattern.vertex_attribute(vertex, "is_fixed", True)
            pattern.vertex_attribute(vertex, "constraints", [str(guid) for guid in guids])

    guids = boundary_guids + hole_guids + segments_guids
    compas_rhino.rs.HideObject(guids)

    group = ui.scene.add(Group(), name="RV3")
    group.add(pattern, name="Pattern")
    ui.scene.active_object = group
    ui.scene.update()
    ui.record()


if __name__ == "__main__":
    RunCommand(True)
