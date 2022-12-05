from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math
import compas_rhino

from compas.topology import breadth_first_traverse
from compas.datastructures import mesh_face_adjacency

from compas_rv3.datastructures import SubdMesh
from compas_rv3.datastructures import Pattern
from compas_rv3.rhino.conduits import SubdConduit

from compas_ui.objects import Group
from compas_ui.ui import UI


__commandname__ = "RV3_pattern_from_surfaces"


def divide_edge_strip_faces(mesh, edge):

    is_strip_quad = True

    strip_edge = mesh.subd_edge_strip(edge)
    edge_strip_faces = mesh.edge_strip_faces(strip_edge)

    for face in edge_strip_faces:
        if not mesh.face_attribute(face, "is_quad"):
            is_strip_quad = False

    if is_strip_quad:
        nu_or_nv = compas_rhino.rs.GetInteger("This is a quadmesh strip - Choose any integer", minimum=2)

    else:
        while True:
            nu_or_nv = compas_rhino.rs.GetInteger(
                "This is a non-quadmesh strip - Choose an integer that is a power of 2",
                minimum=2,
            )
            if (nu_or_nv & (nu_or_nv - 1) == 0) and nu_or_nv != 0:
                break
            else:
                print("Division number has to be power of 2!")

    for face in edge_strip_faces:
        quad = mesh.face_attribute(face, "is_quad")

        if quad:
            u1, u2 = mesh.face_attribute(face, "u_edge")
            v1, v2 = mesh.face_attribute(face, "v_edge")

            if (u1, u2) in strip_edge or (u2, u1) in strip_edge:
                mesh.face_attribute(face, "nu", nu_or_nv)
            else:
                mesh.face_attribute(face, "nv", nu_or_nv)

            if (v1, v2) in strip_edge or (v2, v1) in strip_edge:
                mesh.face_attribute(face, "nv", nu_or_nv)

        else:
            n = math.log(nu_or_nv) / math.log(2)
            mesh.face_attribute(face, "n", int(n))

    return edge_strip_faces


def update_nu_nv(mesh):

    quad_mesh = True

    for face in mesh.faces():
        if not mesh.face_attribute(face, "is_quad"):
            quad_mesh = False

    if quad_mesh:
        nu = compas_rhino.rs.GetInteger("This is a quadmesh - Choose any integer", minimum=2)

        for face in mesh.faces():
            mesh.face_attribute(face, "nu", nu)
            mesh.face_attribute(face, "nv", nu)

    else:
        while True:
            nu_or_nv = compas_rhino.rs.GetInteger("This is a non-quadmesh - Choose an integer that is a power of 2", minimum=2)

            if (nu_or_nv & (nu_or_nv - 1) == 0) and nu_or_nv != 0:
                break
            else:
                print("Division number has to be power of 2!")

        for face in mesh.faces():
            quad = mesh.face_attribute(face, "is_quad")
            if quad:
                mesh.face_attribute(face, "nu", nu_or_nv)
                mesh.face_attribute(face, "nv", nu_or_nv)
            else:
                n = math.log(nu_or_nv) / math.log(2)
                mesh.face_attribute(face, "n", int(n))


def mesh_edge_lines(mesh):
    lines = []
    for u, v in mesh.edges():
        u_xyz = mesh.vertex_coordinates(u)
        v_xyz = mesh.vertex_coordinates(v)
        lines.append([u_xyz, v_xyz])
    return lines


def mesh_unify_cycles(mesh, root=None):
    def unify(node, nbr):
        # find the common edge
        for u, v in mesh.face_halfedges(nbr):
            if u in mesh.face[node] and v in mesh.face[node]:
                # node and nbr have edge u-v in common
                i = mesh.face[node].index(u)
                j = mesh.face[node].index(v)
                if i == j - 1 or (j == 0 and u == mesh.face[node][-1]):
                    # if the traversal of a neighboring halfedge
                    # is in the same direction
                    # flip the neighbor
                    mesh.face[nbr][:] = mesh.face[nbr][::-1]
                    return

    if root is None:
        root = mesh.get_any_face()

    adj = mesh_face_adjacency(mesh)

    breadth_first_traverse(adj, root, unify)

    # assert len(list(visited)) == mesh.number_of_faces(), 'Not all faces were visited'

    mesh.halfedge = {key: {} for key in mesh.vertices()}
    for fkey in mesh.faces():
        for u, v in mesh.face_halfedges(fkey):
            mesh.halfedge[u][v] = fkey
            if u not in mesh.halfedge[v]:
                mesh.halfedge[v][u] = None


@UI.error()
def RunCommand(is_interactive):

    ui = UI()

    # 1. select rhino surface or polysurfaces
    guid = compas_rhino.select_surface(message="Select one surface or joined, non-trimmed surfaces")
    compas_rhino.rs.HideObjects(guid)

    # 2. make subdmesh and add it to the scene
    subdmesh = SubdMesh.from_guid(guid)
    subd = ui.scene.add(subdmesh, name="SubdMesh")
    subd.settings["show.vertices"] = False
    subd.settings["show.edges"] = True
    subd.settings["show.faces"] = False

    # default subdivision
    subdmesh1 = subd.mesh.subdivide_all_faces()

    # 3. setup conduit to temporarily display subdmeshes
    conduit = SubdConduit([])
    conduit.enable()
    conduit.lines = mesh_edge_lines(subdmesh1)
    conduit.thickness = 0
    ui.scene.update()

    # ==========================================================================
    # iterative subdivision
    # ==========================================================================

    options = ["SubdivideEntireMesh", "SubdivideEdgeStrip", "FinishSubdivision"]

    while True:
        option = compas_rhino.rs.GetString("Modify Subdivision", strings=options)

        if option is None:
            conduit.disable()
            ui.scene.clear()
            compas_rhino.rs.ShowObjects(guid)
            print("Subdivision aborted!")
            return

        if not option:
            break

        if option == "SubdivideEntireMesh":
            update_nu_nv(subd.mesh)
            subdmesh1 = subd.mesh.subdivide_all_faces()

        elif option == "SubdivideEdgeStrip":
            edges = subd.select_edges()
            if not edges:
                print("No edge was selected.")
                continue
            edge = edges[0]

            compas_rhino.rs.UnselectAllObjects()
            compas_rhino.rs.Redraw()
            divide_edge_strip_faces(subd.mesh, edge)
            subdmesh1 = subd.mesh.subdivide_all_faces()

        elif option == "FinishSubdivision":
            break

        conduit.lines = mesh_edge_lines(subdmesh1)
        ui.scene.update()

    # ==========================================================================

    conduit.disable()

    # 8. make pattern from subdmesh
    mesh_unify_cycles(subdmesh1)
    pattern = Pattern.from_vertices_and_faces(*subdmesh1.to_vertices_and_faces())

    # 9. update scene
    ui.scene.remove(subd)
    group = ui.scene.add(Group(), name="RV3")
    group.add(pattern, name="Pattern")
    ui.scene.active_object = group
    ui.scene.update()
    ui.record()

    print("Pattern object successfully created. Input surface or polysurface has been hidden.")


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    RunCommand(True)
