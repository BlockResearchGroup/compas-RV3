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

    def __init__(self, *args, **kwargs):
        super(RhinoPatternObject, self).__init__(*args, **kwargs)
        self.add_group(self.groupname_vertices)
        self.add_group(self.groupname_edges)
        self.add_group(self.groupname_faces)

    @RhinoMeshObject.guid_vertex.setter
    def guid_vertex(self, items):
        RhinoMeshObject.guid_vertex.fset(self, items)

        guids = list(self.guid_vertex.keys())
        groupname = self.groupname_vertices

        compas_rhino.rs.AddObjectsToGroup(guids, groupname)
        if self.settings["show.vertices"]:
            compas_rhino.rs.ShowGroup(groupname)
        else:
            compas_rhino.rs.HideGroup(groupname)

    @RhinoMeshObject.guid_edge.setter
    def guid_edge(self, items):
        RhinoMeshObject.guid_edge.fset(self, items)

        guids = list(self.guid_edge.keys())
        groupname = self.groupname_edges

        compas_rhino.rs.AddObjectsToGroup(guids, groupname)
        if self.settings["show.edges"]:
            compas_rhino.rs.ShowGroup(groupname)
        else:
            compas_rhino.rs.HideGroup(groupname)

    @RhinoMeshObject.guid_face.setter
    def guid_face(self, items):
        RhinoMeshObject.guid_face.fset(self, items)

        guids = list(self.guid_face.keys())
        groupname = self.groupname_faces

        compas_rhino.rs.AddObjectsToGroup(guids, groupname)
        if self.settings["show.faces"]:
            compas_rhino.rs.ShowGroup(groupname)
        else:
            compas_rhino.rs.HideGroup(groupname)

    @property
    def groupname_vertices(self):
        return "{}::vertices".format(self.settings["layer"])

    @property
    def groupname_edges(self):
        return "{}::edges".format(self.settings["layer"])

    @property
    def groupname_faces(self):
        return "{}::faces".format(self.settings["layer"])

    @staticmethod
    def add_group(group):
        if not compas_rhino.rs.IsGroup(group):
            compas_rhino.rs.AddGroup(group)

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
        self.artist.vertex_xyz = self.vertex_xyz

        self._draw_vertices()
        self._draw_edges()
        self._draw_faces()

    def _draw_vertices(self):
        vertices = list(self.mesh.vertices())

        color_fixed = self.settings["color.vertices:is_fixed"]
        color_anchor = self.settings["color.vertices:is_anchor"]
        color = {vertex: self.settings["color.vertices"] for vertex in vertices}
        color.update({vertex: color_fixed for vertex in self.mesh.vertices_where(is_fixed=True)})
        color.update({vertex: color_anchor for vertex in self.mesh.vertices_where(is_anchor=True)})

        guids = self.artist.draw_vertices(vertices, color)
        self.guids += guids
        self.guid_vertex = zip(guids, vertices)

    def _draw_edges(self):
        edges = list(self.mesh.edges())
        color = {edge: self.settings["color.edges"] for edge in edges}
        guids = self.artist.draw_edges(edges, color)
        self.guids += guids
        self.guid_edge = zip(guids, edges)

    def _draw_faces(self):
        faces = list(self.mesh.faces())
        color = {face: self.settings["color.faces"] for face in faces}
        guids = self.artist.draw_faces(faces, color)
        self.guids += guids
        self.guid_face = zip(guids, faces)
