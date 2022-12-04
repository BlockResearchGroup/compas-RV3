from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv3.objects import DiagramObject
from compas_ui.rhino.objects import RhinoMeshObject


class RhinoDiagramObject(RhinoMeshObject, DiagramObject):
    """
    Rhino scene object for diagrams in RV3.

    Attributes
    ----------
    groupname_vertices : str
        The name of the group containing the vertices.
    groupname_edges : str
        The name of the group containing the edges.
    groupname_faces : str
        The name of the group containing the faces.

    """

    def __init__(self, *args, **kwargs):
        super(RhinoDiagramObject, self).__init__(*args, **kwargs)
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
        """
        Mark the point objects in Rhino corresponding to certain diagram vertices as selected.

        Parameters
        ----------
        vertices : list[int]
            The identifiers of the diagram vertices.

        Returns
        -------
        None

        """
        guids = []
        for guid, vertex in self.guid_vertex.items():
            if vertex in vertices:
                guids.append(guid)
        compas_rhino.rs.UnselectAllObjects()
        compas_rhino.rs.EnableRedraw(False)
        compas_rhino.rs.SelectObjects(guids)
        compas_rhino.rs.EnableRedraw(True)

    def select_edge_lines(self, edges):
        """
        Mark the line objects in Rhino corresponding to certain diagram edges as selected.

        Parameters
        ----------
        edges : list[tuple[int, int]]
            The identifiers of the diagram edges.

        Returns
        -------
        None

        """
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
        """
        Mark the mesh objects in Rhino corresponding to certain diagram faces as selected.

        Parameters
        ----------
        faces : list[int]
            The identifiers of the diagram faces.

        Returns
        -------
        None

        """
        guids = []
        for guid, face in self.guid_face.items():
            if face in faces:
                guids.append(guid)
        compas_rhino.rs.UnselectAllObjects()
        compas_rhino.rs.EnableRedraw(False)
        compas_rhino.rs.SelectObjects(guids)
        compas_rhino.rs.EnableRedraw(True)
