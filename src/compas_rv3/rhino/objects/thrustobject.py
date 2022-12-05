from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.colors import Color
from compas.utilities import remap_values
from compas_rv3.objects import ThrustObject
from compas_rv3.rhino.conduits import SelfWeightConduit
from compas_rv3.rhino.conduits import ReactionConduit
from compas_rv3.rhino.conduits import ResidualConduit
from compas_rv3.rhino.conduits import LoadConduit
from .diagramobject import RhinoDiagramObject


class RhinoThrustObject(RhinoDiagramObject, ThrustObject):
    """
    Rhino scene object for form diagrams in RV3.

    Attributes
    ----------
    groupname_vertices_free : str, readonly
        The name of the group containing the non-anchored vertices.
    groupname_vertices_anchored : str, readonly
        The name of the group containing the anchored vertices.
    conduit_selfweight : :class:`compas_rv3.rhino.conduits.SelfWeightConduit`, readonly
        Conduit for displaying selfweight vectors.
    conduit_loads : :class:`compas_rv3.rhino.conduits.LoadConduit`, readonly
        Conduit for displaying load vectors.
    conduit_reactions : :class:`compas_rv3.rhino.conduits.ReactionConduit`, readonly
        Conduit for displaying reaction vectors.
    conduit_residuals : :class:`compas_rv3.rhino.conduits.ResidualConduit`, readonly
        Conduit for displaying residual vectors.

    """

    def __init__(self, *args, **kwargs):
        super(RhinoThrustObject, self).__init__(*args, **kwargs)
        self._conduit_selfweight = None
        self._conduit_reactions = None
        self._conduit_loads = None
        self._conduit_residuals = None
        self.add_group(self.groupname_vertices_free)
        self.add_group(self.groupname_vertices_anchored)

    @property
    def groupname_vertices_free(self):
        return "{}::vertices::free".format(self.settings["layer"])

    @property
    def groupname_vertices_anchored(self):
        return "{}::vertices::anchored".format(self.settings["layer"])

    @property
    def conduit_selfweight(self):
        if self._conduit_selfweight is None:
            self._conduit_selfweight = SelfWeightConduit(
                self.diagram,
                color=self.settings["color.selfweight"],
                scale=self.settings["scale.selfweight"],
                tol=self.settings["tol.selfweight"],
            )
        return self._conduit_selfweight

    @property
    def conduit_reactions(self):
        if self._conduit_reactions is None:
            self._conduit_reactions = ReactionConduit(
                self.diagram,
                color=self.settings["color.reactions"],
                scale=self.settings["scale.externalforces"],
                tol=self.settings["tol.externalforces"],
            )
        return self._conduit_reactions

    @property
    def conduit_loads(self):
        if self._conduit_loads is None:
            self._conduit_loads = LoadConduit(
                self.diagram,
                color=self.settings["color.loads"],
                scale=self.settings["scale.externalforces"],
                tol=self.settings["tol.externalforces"],
            )
        return self._conduit_loads

    @property
    def conduit_residuals(self):
        if self._conduit_residuals is None:
            self._conduit_residuals = ResidualConduit(
                self.diagram,
                color=self.settings["color.residuals"],
                scale=self.settings["scale.residuals"],
                tol=self.settings["tol.residuals"],
            )
        return self._conduit_residuals

    @RhinoDiagramObject.guid_vertex.setter
    def guid_vertex(self, items):
        RhinoDiagramObject.guid_vertex.fset(self, items)

        guids_free = [guid for guid, vertex in items if not self.diagram.vertex_attribute(vertex, "is_anchor")]
        guids_anchored = [guid for guid, vertex in items if self.diagram.vertex_attribute(vertex, "is_anchor")]

        compas_rhino.rs.AddObjectsToGroup(guids_free, self.groupname_vertices_free)
        compas_rhino.rs.AddObjectsToGroup(guids_anchored, self.groupname_vertices_anchored)
        compas_rhino.rs.HideGroup(self.groupname_vertices_free)

        if self.settings["show.vertices"]:
            compas_rhino.rs.ShowGroup(self.groupname_vertices_anchored)
        else:
            compas_rhino.rs.HideGroup(self.groupname_vertices_anchored)

    def clear_conduits(self):
        """
        Clear all the conduits.

        Returns
        -------
        None

        """
        try:
            self.conduit_selfweight.disable()
        except Exception:
            pass
        # finally:
        #     del self._conduit_selfweight
        #     self._conduit_selfweight = None

        try:
            self.conduit_reactions.disable()
        except Exception:
            pass
        # finally:
        #     del self._conduit_reactions
        #     self._conduit_reactions = None

        try:
            self.conduit_loads.disable()
        except Exception:
            pass
        # finally:
        #     del self._conduit_loads
        #     self._conduit_loads = None

        try:
            self.conduit_residuals.disable()
        except Exception:
            pass
        # finally:
        #     del self._conduit_residuals
        #     self._conduit_residuals = None

    def clear(self):
        """
        Clear the objects previously drawn by this object.

        Returns
        -------
        None

        """
        super(RhinoThrustObject, self).clear()
        self.clear_conduits()

    def draw(self):
        """
        Draw the objects representing the thrust diagram.

        Returns
        -------
        None

        """
        self.clear()
        if not self.visible:
            return

        layer = self.settings["layer"]
        self.artist.layer = layer
        self.artist.vertex_xyz = self.vertex_xyz

        self._draw_vertices()
        self._draw_edges()
        self._draw_mesh()
        self._draw_pipes()
        self._draw_overlays()

    def _draw_vertices(self):
        free = list(self.diagram.vertices_where(is_anchor=False))
        fixed = list(self.diagram.vertices_where(is_fixed=True))
        anchored = list(self.diagram.vertices_where(is_anchor=True))

        color_free = self.settings["color.vertices"]
        color_fixed = self.settings["color.vertices:is_fixed"]
        color_anchor = self.settings["color.vertices:is_anchor"]
        if not self.is_valid:
            color_free = self.settings["color.invalid"]

        color = {}
        color.update({vertex: color_free for vertex in free})
        color.update({vertex: color_fixed for vertex in fixed})
        color.update({vertex: color_anchor for vertex in anchored})

        guids_free = self.artist.draw_vertices(free, color)
        guids_anchored = self.artist.draw_vertices(anchored, color)

        guids = guids_free + guids_anchored
        vertices = free + anchored
        self.guids += guids
        self.guid_vertex = zip(guids, vertices)

    def _draw_edges(self):
        if not self.settings["show.edges"]:
            return

        edges = list(self.diagram.edges_where(_is_edge=True))
        color = self.settings["color.edges"] if self.is_valid else self.settings["color.invalid"]
        edge_color = {edge: color for edge in edges}

        if self.ui.registry["RV3"]["show.forces"]:
            if self.diagram.dual:
                _edges = list(self.diagram.dual.edges())
                edges = [self.diagram.dual.primal_edge(edge) for edge in _edges]
                lengths = remap_values([self.diagram.dual.edge_length(*edge) for edge in _edges])
                edge_color.update({edge: Color.from_i(value) for edge, value in zip(edges, lengths)})

        guids = self.artist.draw_edges(edges, edge_color)
        self.guids += guids
        self.guid_edge = zip(guids, edges)

    def _draw_faces(self):
        if not self.settings["show.faces"]:
            return

        faces = list(self.diagram.faces_where(_is_loaded=True))

        if self.is_valid:
            if self.settings["show.stresses"]:
                vertices = list(self.diagram.vertices())
                stresses = remap_values([self.diagram.vertex_lumped_stress(vertex) for vertex in vertices])
                color = self.settings["color.invalid"].rgb255
                vertex_color = {vertex: color for vertex in vertices}
                vertex_color.update({vertex: Color.from_i(value).rgb255 for vertex, value in zip(vertices, stresses)})

                facets = []
                for face in faces:
                    points = self.diagram.face_coordinates(face)
                    name = "{}.face.{}".format(self.diagram.name, face)
                    vertexcolors = [vertex_color[vertex] for vertex in self.diagram.face_vertices(face)]
                    facets.append({"points": points, "name": name, "vertexcolors": vertexcolors})
                guids = compas_rhino.draw_faces(facets, layer=self.settings["layer"], clear=False, redraw=False)

            else:
                color = self.settings["color.faces"]
                face_color = {face: color for face in faces}
                guids = self.artist.draw_faces(faces, face_color)

        else:
            color = self.settings["color.invalid"]
            face_color = {face: color for face in faces}
            guids = self.artist.draw_faces(faces, face_color)

        self.guids += guids
        self.guid_face = zip(guids, faces)

    def _draw_mesh(self):
        vertices = list(self.diagram.vertices())

        if self.is_valid:
            if self.ui.registry["RV3"]["show.forces"]:
                color = Color.white().rgb255
                vertex_color = {vertex: color for vertex in vertices}
            elif self.settings["show.stresses"]:
                stresses = remap_values([self.diagram.vertex_lumped_stress(vertex) for vertex in vertices])
                color = self.settings["color.invalid"].rgb255
                vertex_color = {vertex: color for vertex in vertices}
                vertex_color.update({vertex: Color.from_i(value).rgb255 for vertex, value in zip(vertices, stresses)})
            else:
                color = self.settings["color.faces"].rgb255
                vertex_color = {vertex: color for vertex in vertices}
        else:
            color = self.settings["color.invalid"].rgb255
            vertex_color = {vertex: color for vertex in vertices}

        faces = [self.diagram.face_vertices(face) for face in self.diagram.faces_where(_is_loaded=True)]
        guid = compas_rhino.draw_mesh(
            {vertex: self.diagram.vertex_coordinates(vertex) for vertex in vertices},
            faces,
            disjoint=True,
            color=color,
            vertex_color=vertex_color,
        )
        self.guids += [guid]

    def _draw_pipes(self):
        if not self.is_valid:
            return
        if not self.settings["show.pipes"]:
            return

        tol = self.settings["tol.pipes"]
        edges = list(self.diagram.edges_where(_is_edge=True))
        edge_color = {edge: self.settings["color.pipes"] for edge in edges}

        if self.ui.registry["RV3"]["show.forces"]:
            if self.diagram.dual:
                _edges = list(self.diagram.dual.edges())
                lengths = remap_values([self.diagram.dual.edge_length(*edge) for edge in _edges])
                edges = [self.diagram.dual.primal_edge(edge) for edge in _edges]
                edge_color.update({edge: Color.from_i(value) for edge, value in zip(edges, lengths)})

        scale = self.settings["scale.pipes"]
        guids = self.artist.draw_pipes(edges, edge_color, scale, tol)
        self.guids += guids

    # ======================================================================
    # Overlays
    # --------
    # Color overlays for various display modes.
    # ======================================================================

    def _draw_overlays(self):
        # selfweight
        self.conduit_selfweight.disable()
        if self.is_valid and self.settings["show.selfweight"]:
            self.conduit_selfweight.color = self.settings["color.selfweight"].rgb255
            self.conduit_selfweight.scale = self.settings["scale.selfweight"]
            self.conduit_selfweight.tol = self.settings["tol.selfweight"]
            self.conduit_selfweight.enable()
        # loads
        self.conduit_loads.disable()
        if self.is_valid and self.settings["show.loads"]:
            self.conduit_loads.color = self.settings["color.loads"].rgb255
            self.conduit_loads.scale = self.settings["scale.externalforces"]
            self.conduit_loads.tol = self.settings["tol.externalforces"]
            self.conduit_loads.enable()
        # residuals
        self.conduit_residuals.disable()
        if self.is_valid and self.settings["show.residuals"]:
            self.conduit_residuals.color = self.settings["color.residuals"].rgb255
            self.conduit_residuals.scale = self.settings["scale.residuals"]
            self.conduit_residuals.tol = self.settings["tol.residuals"]
            self.conduit_residuals.enable()
        # reactions
        self.conduit_reactions.disable()
        if self.is_valid and self.settings["show.reactions"]:
            self.conduit_reactions.color = self.settings["color.reactions"].rgb255
            self.conduit_reactions.scale = self.settings["scale.externalforces"]
            self.conduit_reactions.tol = self.settings["tol.externalforces"]
            self.conduit_reactions.enable()

    # ======================================================================
    # Rhino View Control
    # ======================================================================

    def select_vertices_free(self):
        """
        Manually select free vertices in the Rhino model view.

        Returns
        -------
        list[int]
            The identifiers of the selected vertices.

        """
        free = []
        guids = compas_rhino.select_points(message="Select free vertices.")
        if guids:
            vertices = [self.guid_vertex[guid] for guid in guids if guid in self.guid_vertex]
            free = [vertex for vertex in vertices if not self.diagram.vertex_attribute(vertex, "is_anchor")]
        return free

    def select_vertices_anchor(self):
        """
        Manually select anchor vertices in the Rhino model view.

        Returns
        -------
        list[int]
            The identifiers of the selected vertices.

        """
        anchors = []
        guids = compas_rhino.select_points(message="Select anchor vertices.")
        if guids:
            vertices = [self.guid_vertex[guid] for guid in guids if guid in self.guid_vertex]
            anchors = [vertex for vertex in vertices if self.diagram.vertex_attribute(vertex, "is_anchor")]
        return anchors
