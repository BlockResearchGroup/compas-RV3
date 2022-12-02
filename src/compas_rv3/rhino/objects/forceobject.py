from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.colors import Color
from compas_ui.ui import UI
from compas_rv3.objects import ForceObject
from .diagramobject import RhinoDiagramObject


class RhinoForceObject(RhinoDiagramObject, ForceObject):
    """
    Rhino scene object for force diagrams in RV3.
    """

    def draw(self):
        """
        Draw the objects representing the force diagram.
        """
        ui = UI()

        self.clear()
        if not self.visible:
            return

        layer = self.settings["layer"]
        self.artist.layer = layer
        self.artist.clear_layer()
        self.artist.vertex_xyz = self.vertex_xyz

        group_vertices = "{}::vertices".format(layer)
        group_edges = "{}::edges".format(layer)

        if not compas_rhino.rs.IsGroup(group_vertices):
            compas_rhino.rs.AddGroup(group_vertices)

        if not compas_rhino.rs.IsGroup(group_edges):
            compas_rhino.rs.AddGroup(group_edges)

        vertices = list(self.diagram.vertices())
        color = {vertex: self.settings["color.vertices"] for vertex in vertices}
        guids = self.artist.draw_vertices(vertices, color)
        self.guids += guids
        self.guid_vertex = zip(guids, vertices)

        compas_rhino.rs.AddObjectsToGroup(guids, group_vertices)

        if self.settings["show.vertices"]:
            compas_rhino.rs.ShowGroup(group_vertices)
        else:
            compas_rhino.rs.HideGroup(group_vertices)

        edges = list(self.diagram.edges())
        colors = {}
        for edge in edges:
            primal = self.diagram.primal_edge(edge)
            if self.diagram.primal.edge_attribute(primal, "_is_tension"):
                colors[edge] = self.settings["color.tension"]
            else:
                colors[edge] = self.settings["color.edges"]

        if ui.registry["RV3"]["show.forces"]:
            lengths = [self.diagram.edge_length(*edge) for edge in edges]
            lmin = min(lengths)
            lmax = max(lengths)
            for edge, length in zip(edges, lengths):
                if lmin != lmax:
                    colors[edge] = Color.from_i((length - lmin) / (lmax - lmin))

        guids = self.artist.draw_edges(edges, colors)
        self.guids += guids
        self.guid_edge = zip(guids, edges)

        compas_rhino.rs.AddObjectsToGroup(guids, group_edges)

        if self.settings["show.edges"]:
            compas_rhino.rs.ShowGroup(group_edges)
        else:
            compas_rhino.rs.HideGroup(group_edges)

        if ui.registry["RV3"]["show.angles"]:
            tol = ui.registry["RV3"]["tol.angles"]
            edges = list(self.diagram.edges())
            angles = self.diagram.edges_attribute("_a", keys=edges)
            amin = min(angles)
            amax = max(angles)
            if (amax - amin) ** 2 > 0.001**2:
                text = {}
                color = {}
                for edge, angle in zip(edges, angles):
                    if angle > tol:
                        text[edge] = "{:.0f}".format(angle)
                        color[edge] = Color.from_i((angle - amin) / (amax - amin))
                # what about colors?
                guids = self.artist.draw_edgelabels(text)
                self.guids += guids
