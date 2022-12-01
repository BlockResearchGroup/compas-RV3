from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv3.objects import PatternObject
from compas_ui.rhino.objects import RhinoMeshObject


class RhinoPatternObject(RhinoMeshObject, PatternObject):
    """
    Rhino scene object for patterns in RV3.
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

    def draw(self):
        """
        Draw the objects representing the force diagram.
        """
        self.clear()
        if not self.visible:
            return
        layer = self.settings["layer"]
        self.artist.layer = layer
        self.artist.clear_layer()
        self.artist.vertex_xyz = self.vertex_xyz

        if self.settings["show.vertices"]:
            color_fixed = self.settings["color.vertices:is_fixed"]
            color_anchor = self.settings["color.vertices:is_anchor"]
            vertices = list(self.mesh.vertices())
            color = {vertex: self.settings["color.vertices"] for vertex in vertices}
            color.update({vertex: color_fixed for vertex in self.mesh.vertices_where(is_fixed=True)})
            color.update({vertex: color_anchor for vertex in self.mesh.vertices_where(is_anchor=True)})

            guids = self.artist.draw_vertices(vertices, color)
            self.guids += guids
            self.guid_vertex = zip(guids, vertices)

        if self.settings["show.edges"]:
            edges = list(self.mesh.edges())
            color = {edge: self.settings["color.edges"] for edge in edges}

            guids = self.artist.draw_edges(edges, color)
            self.guids += guids
            self.guid_edge = zip(guids, edges)

        if self.settings["show.faces"]:
            faces = list(self.mesh.faces())
            color = {face: self.settings["color.faces"] for face in faces}

            guids = self.artist.draw_faces(faces, color)
            self.guids += guids
            self.guid_face = zip(guids, faces)
