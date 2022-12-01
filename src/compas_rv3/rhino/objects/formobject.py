from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.colors import Color
from compas_rv3.objects import FormObject
from .diagramobject import RhinoDiagramObject


class RhinoFormObject(RhinoDiagramObject, FormObject):
    """
    Rhino scene object for form diagrams in RV3.
    """

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
            vertices = list(self.mesh.vertices())
            color = {vertex: self.settings["color.vertices"] for vertex in vertices}
            color_fixed = self.settings["color.vertices:is_fixed"]
            color_anchor = self.settings["color.vertices:is_anchor"]
            color.update({vertex: color_fixed for vertex in self.mesh.vertices_where(is_fixed=True) if vertex in vertices})
            color.update({vertex: color_anchor for vertex in self.mesh.vertices_where(is_anchor=True) if vertex in vertices})

            guids = self.artist.draw_vertices(vertices, color)
            self.guids += guids
            self.guid_vertex = zip(guids, vertices)

        if self.settings["show.edges"]:
            edges = list(self.mesh.edges_where({"_is_edge": True}))
            colors = {}

            for edge in edges:
                if self.mesh.edge_attribute(edge, "_is_tension"):
                    colors[edge] = self.settings["color.tension"]
                else:
                    colors[edge] = self.settings["color.edges"]

            if self.scene and self.scene.settings["RV2"]["show.forces"]:
                if self.mesh.dual:
                    _edges = list(self.mesh.dual.edges())
                    lengths = [self.mesh.dual.edge_length(*edge) for edge in _edges]
                    edges = [self.mesh.dual.primal_edge(edge) for edge in _edges]
                    lmin = min(lengths)
                    lmax = max(lengths)
                    for edge, length in zip(edges, lengths):
                        if lmin != lmax:
                            i = (length - lmin) / (lmax - lmin)
                            colors[edge] = Color.from_i(i)

            guids = self.artist.draw_edges(edges, colors)
            self.guids += guids
            self.guid_edge = zip(guids, edges)

        # if self.scene and self.scene.settings["RV2"]["show.angles"]:
        #     tol = self.scene.settings["RV2"]["tol.angles"]
        #     edges = list(self.mesh.edges_where({"_is_edge": True}))
        #     angles = self.mesh.edges_attribute("_a", keys=edges)
        #     amin = min(angles)
        #     amax = max(angles)
        #     if (amax - amin) ** 2 > 0.001**2:
        #         text = {}
        #         color = {}
        #         for edge, angle in zip(edges, angles):
        #             if angle > tol:
        #                 text[edge] = "{:.0f}".format(angle)
        #                 color[edge] = i_to_rgb((angle - amin) / (amax - amin))
        #         guids = self.artist.draw_edgelabels(text, color)
        #         self.guid_edgelabel = zip(guids, edges)
