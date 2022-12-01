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

        if self.settings["show.vertices"]:
            vertices = list(self.diagram.vertices())
            color = {}
            color_free = self.settings["color.vertices"] if self.is_valid else self.settings["color.invalid"]
            color_anchor = self.settings["color.vertices:is_anchor"]
            color.update({vertex: color_free for vertex in self.diagram.vertices()})
            color.update({vertex: color_anchor for vertex in self.diagram.vertices_where(is_anchor=True)})
            guids = self.artist.draw_vertices(color)
            self.guids += guids
            self.guid_vertex = zip(guids, vertices)

        if self.settings["show.edges"]:
            edges = list(self.diagram.edges_where({"_is_edge": True}))
            color = {edge: self.settings["color.edges"] if self.is_valid else self.settings["color.invalid"] for edge in edges}

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
            guids = self.artist.draw_edges(edges, color)
            self.guids += guids
            self.guid_edge = zip(guids, edges)

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
                guids = compas_rhino.draw_faces(facets, layer=self.layer, clear=False, redraw=False)

            else:
                guids = self.artist.draw_faces(faces, color)

            self.guids += guids
            self.guid_face = zip(guids, faces)

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

        # if self.is_valid and self.settings["show.pipes"]:
        #     tol = self.settings["tol.pipes"]
        #     edges = list(self.diagram.edges_where({"_is_edge": True}))
        #     color = {edge: self.settings["color.pipes"] for edge in edges}

        #     # color analysis
        #     if self.scene and self.scene.settings["RV2"]["show.forces"]:
        #         if self.diagram.dual:
        #             _edges = list(self.diagram.dual.edges())
        #             lengths = [self.diagram.dual.edge_length(*edge) for edge in _edges]
        #             edges = [self.diagram.dual.primal_edge(edge) for edge in _edges]
        #             lmin = min(lengths)
        #             lmax = max(lengths)
        #             for edge, length in zip(edges, lengths):
        #                 if lmin != lmax:
        #                     color[edge] = i_to_rgb((length - lmin) / (lmax - lmin))

        #     scale = self.settings["scale.pipes"]
        #     guids = self.artist.draw_pipes(edges, color, scale, tol)
        #     self.guid_pipe = zip(guids, edges)

    # def select_vertices_free(self):
    #     """Manually select free vertices in the Rhino model view.

    #     Returns
    #     -------
    #     list
    #         The keys of the selected vertices.

    #     Examples
    #     --------
    #     >>>
    #     """
    #     guids = compas_rhino.select_points(message="Select free vertices.")
    #     if guids:
    #         keys = [self.guid_free[guid] for guid in guids if guid in self.guid_free]
    #     else:
    #         keys = []
    #     return keys

    # def select_vertices_anchor(self):
    #     """Manually select anchor vertices in the Rhino model view.

    #     Returns
    #     -------
    #     list
    #         The keys of the selected vertices.

    #     Examples
    #     --------
    #     >>>
    #     """
    #     guids = compas_rhino.select_points(message="Select anchor vertices.")
    #     if guids:
    #         keys = [self.guid_anchor[guid] for guid in guids if guid in self.guid_anchor]
    #     else:
    #         keys = []
    #     return keys
