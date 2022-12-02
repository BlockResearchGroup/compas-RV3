from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.colors import Color
from compas_ui.ui import UI
from compas_rv3.objects import ThrustObject
from compas_rv3.rhino.conduits import SelfWeightConduit
from compas_rv3.rhino.conduits import ReactionConduit
from compas_rv3.rhino.conduits import ResidualConduit
from compas_rv3.rhino.conduits import LoadConduit
from .diagramobject import RhinoDiagramObject


class RhinoThrustObject(RhinoDiagramObject, ThrustObject):
    """
    Rhino scene object for form diagrams in RV3.
    """

    def __init__(self, *args, **kwargs):
        super(RhinoThrustObject, self).__init__(*args, **kwargs)
        self._conduit_selfweight = None
        self._conduit_reactions = None
        self._conduit_loads = None
        self._conduit_residuals = None

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

    def clear_conduits(self):
        try:
            self.conduit_selfweight.disable()
        except Exception:
            pass
        finally:
            del self._conduit_selfweight
            self._conduit_selfweight = None

        try:
            self.conduit_reactions.disable()
        except Exception:
            pass
        finally:
            del self._conduit_reactions
            self._conduit_reactions = None

        try:
            self.conduit_loads.disable()
        except Exception:
            pass
        finally:
            del self._conduit_loads
            self._conduit_loads = None

        try:
            self.conduit_residuals.disable()
        except Exception:
            pass
        finally:
            del self._conduit_residuals
            self._conduit_residuals = None

    def clear(self):
        super(RhinoThrustObject, self).clear()
        self.clear_conduits()

    def draw(self):
        """Draw the objects representing the thrust diagram."""
        ui = UI()

        self.clear()
        if not self.visible:
            return

        layer = self.settings["layer"]
        self.artist.layer = layer
        self.artist.clear_layer()
        self.artist.vertex_xyz = self.vertex_xyz

        group_free = "{}::vertices_free".format(layer)
        group_anchor = "{}::vertices_anchor".format(layer)

        group_edges = "{}::edges".format(layer)
        group_faces = "{}::faces".format(layer)

        if not compas_rhino.rs.IsGroup(group_free):
            compas_rhino.rs.AddGroup(group_free)

        if not compas_rhino.rs.IsGroup(group_anchor):
            compas_rhino.rs.AddGroup(group_anchor)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        if not compas_rhino.rs.IsGroup(group_faces):
            compas_rhino.rs.AddGroup(group_faces)

        free = list(self.diagram.vertices_where(is_anchor=False))
        anchors = list(self.diagram.vertices_where(is_anchor=True))
        color = {}
        color_free = self.settings["color.vertices"] if self.is_valid else self.settings["color.invalid"]
        color_fixed = self.settings["color.vertices:is_fixed"]
        color_anchor = self.settings["color.vertices:is_anchor"]
        color.update({vertex: color_free for vertex in free})
        color.update({vertex: color_fixed for vertex in self.diagram.vertices_where(is_fixed=True)})
        color.update({vertex: color_anchor for vertex in anchors})
        guids_free = self.artist.draw_vertices(free, color)
        guids_anchors = self.artist.draw_vertices(anchors, color)
        guids = guids_free + guids_anchors
        vertices = free + anchors
        self.guids += guids
        self.guid_vertex = zip(guids, vertices)

        compas_rhino.rs.AddObjectsToGroup(guids_free, group_free)
        compas_rhino.rs.AddObjectsToGroup(guids_anchors, group_anchor)

        if self.settings["show.vertices"]:
            compas_rhino.rs.HideGroup(group_free)
            compas_rhino.rs.ShowGroup(group_anchor)
        else:
            compas_rhino.rs.HideGroup(group_free)
            compas_rhino.rs.HideGroup(group_anchor)

        edges = list(self.diagram.edges_where(_is_edge=True))
        color = {edge: self.settings["color.edges"] if self.is_valid else self.settings["color.invalid"] for edge in edges}

        if ui.registry["RV3"]["show.forces"]:
            if self.diagram.dual:
                _edges = list(self.diagram.dual.edges())
                lengths = [self.diagram.dual.edge_length(*edge) for edge in _edges]
                edges = [self.diagram.dual.primal_edge(edge) for edge in _edges]
                lmin = min(lengths)
                lmax = max(lengths)
                for edge, length in zip(edges, lengths):
                    if lmin != lmax:
                        color[edge] = Color.from_i((length - lmin) / (lmax - lmin))
        guids = self.artist.draw_edges(edges, color)
        self.guids += guids
        self.guid_edge = zip(guids, edges)

        compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        if self.settings["show.edges"]:
            compas_rhino.rs.ShowGroup(group_edges)
        else:
            compas_rhino.rs.HideGroup(group_edges)

        if self.settings["show.faces"]:
            faces = list(self.diagram.faces_where(_is_loaded=True))
            color = {face: self.settings["color.faces"] if self.is_valid else self.settings["color.invalid"] for face in faces}

            if self.is_valid and self.settings["show.stresses"]:
                vertices = list(self.diagram.vertices())
                vertex_colors = {vertex: self.settings["color.vertices"] if self.is_valid else self.settings["color.invalid"] for vertex in vertices}
                stresses = [self.diagram.vertex_lumped_stress(vertex) for vertex in vertices]
                smin = min(stresses)
                smax = max(stresses)

                for vertex, stress in zip(vertices, stresses):
                    if smin != smax:
                        vertex_colors[vertex] = Color.from_i((stress - smin) / (smax - smin))

                facets = []
                for face in faces:
                    facets.append(
                        {
                            "points": self.diagram.face_coordinates(face),
                            "name": "{}.face.{}".format(self.diagram.name, face),
                            "vertexcolors": [vertex_colors[vertex] for vertex in self.diagram.face_vertices(face)],
                        }
                    )
                guids = compas_rhino.draw_faces(facets, layer=self.settings["layer"], clear=False, redraw=False)

            else:
                guids = self.artist.draw_faces(faces, color)

            self.guids += guids
            self.guid_face = zip(guids, faces)

            compas_rhino.rs.AddObjectsToGroup(guids, group_faces)
            compas_rhino.rs.ShowGroup(group_faces)

        else:
            compas_rhino.rs.HideGroup(group_faces)

        # ======================================================================
        # Overlays
        # --------
        # Color overlays for various display modes.
        # ======================================================================

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

        if self.is_valid and self.settings["show.pipes"]:
            tol = self.settings["tol.pipes"]
            edges = list(self.diagram.edges_where(_is_edge=True))
            color = {edge: self.settings["color.pipes"] for edge in edges}

            # color analysis
            if ui.registry["RV3"]["show.forces"]:
                if self.diagram.dual:
                    _edges = list(self.diagram.dual.edges())
                    lengths = [self.diagram.dual.edge_length(*edge) for edge in _edges]
                    edges = [self.diagram.dual.primal_edge(edge) for edge in _edges]
                    lmin = min(lengths)
                    lmax = max(lengths)
                    for edge, length in zip(edges, lengths):
                        if lmin != lmax:
                            color[edge] = Color.from_i((length - lmin) / (lmax - lmin))

            scale = self.settings["scale.pipes"]
            guids = self.artist.draw_pipes(edges, color, scale, tol)
            self.guids += guids

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
