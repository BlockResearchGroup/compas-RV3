from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv3.objects import DiagramObject
from compas_ui.rhino.objects import RhinoMeshObject


class RhinoDiagramObject(RhinoMeshObject, DiagramObject):
    """
    Rhino scene object for diagrams in RV3.
    """

    def select_vertex_points(self, vertices):
        guids = []
        for guid, vertex in self.guid_vertex.items():
            if vertex in vertices:
                guids.append(guid)
        compas_rhino.rs.UnselectAllObjects()
        compas_rhino.rs.EnableRedraw(False)
        compas_rhino.rs.SelectObjects(guids)
        compas_rhino.rs.EnableRedraw(True)

    def select_edge_lines(self, edges):
        guids = []
        for guid, (u, v) in self.guid_edge.items():
            if (u, v) in edges:
                guids.append(guid)
            elif (v, u) in edges:
                guids.append(guid)
        compas_rhino.rs.UnselectAllObjects()
        compas_rhino.rs.EnableRedraw(False)
        compas_rhino.rs.SelectObjects(guids)
        compas_rhino.rs.EnableRedraw(True)

    def select_face_meshes(self, faces):
        guids = []
        for guid, face in self.guid_face.items():
            if face in faces:
                guids.append(guid)
        compas_rhino.rs.UnselectAllObjects()
        compas_rhino.rs.EnableRedraw(False)
        compas_rhino.rs.SelectObjects(guids)
        compas_rhino.rs.EnableRedraw(True)
