from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.colors import Color
from compas.geometry import centroid_points

from compas_rv3.objects import FormObject
from .diagramobject import RhinoDiagramObject


class RhinoFormObject(RhinoDiagramObject, FormObject):
    """
    Rhino scene object for form diagrams in RV3.
    """

    def draw(self):
        """
        Draw the objects representing the form diagram.
        """
        self.clear()
        if not self.visible:
            return

        layer = self.settings["layer"]
        self.artist.layer = layer
        self.artist.vertex_xyz = self.vertex_xyz

        self.add_group_for_vertices()
        self.add_group_for_edges()

        self._draw_vertices()
        self._draw_edges()
        self._draw_edgelabels()

    def _draw_vertices(self):
        """
        Draw the vertices of the diagram.
        This implementation is different than the base implementation for a normal mesh object.
        All vertices are drawn and added to a group.
        Visibility is controlled by showing or hiding the group.

        Returns
        -------
        None

        """
        vertices = list(self.diagram.vertices())
        color = {vertex: self.settings["color.vertices"] for vertex in vertices}
        color_fixed = self.settings["color.vertices:is_fixed"]
        color_anchor = self.settings["color.vertices:is_anchor"]
        color.update({vertex: color_fixed for vertex in self.diagram.vertices_where(is_fixed=True) if vertex in vertices})
        color.update({vertex: color_anchor for vertex in self.diagram.vertices_where(is_anchor=True) if vertex in vertices})

        guids = self.artist.draw_vertices(vertices, color)
        self.guids += guids
        self.guid_vertex = zip(guids, vertices)

        compas_rhino.rs.AddObjectsToGroup(guids, self.group_vertices)
        if self.settings["show.vertices"]:
            compas_rhino.rs.ShowGroup(self.group_vertices)
        else:
            compas_rhino.rs.HideGroup(self.group_vertices)

    def _draw_edges(self):
        """
        Draw the edges of the diagram.
        This implementation is different than the base implementation for a normal mesh object.
        All edges are drawn and added to a group.
        Visibility is controlled by showing or hiding the group.

        Returns
        -------
        None

        """
        edges = list(self.diagram.edges_where(_is_edge=True))
        colors = {}
        for edge in edges:
            if self.diagram.edge_attribute(edge, "_is_tension"):
                colors[edge] = self.settings["color.tension"]
            else:
                colors[edge] = self.settings["color.edges"]

        if self.ui.registry["RV3"]["show.forces"]:
            if self.diagram.dual:
                _edges = list(self.diagram.dual.edges())
                lengths = [self.diagram.dual.edge_length(*edge) for edge in _edges]
                edges = [self.diagram.dual.primal_edge(edge) for edge in _edges]
                lmin = min(lengths)
                lmax = max(lengths)
                if lmin != lmax:
                    lspan = lmax - lmin
                    for edge, length in zip(edges, lengths):
                        i = (length - lmin) / lspan
                        colors[edge] = Color.from_i(i)

        guids = self.artist.draw_edges(edges, colors)
        self.guids += guids
        self.guid_edge = zip(guids, edges)

        compas_rhino.rs.AddObjectsToGroup(guids, self.group_edges)
        if self.settings["show.edges"]:
            compas_rhino.rs.ShowGroup(self.group_edges)
        else:
            compas_rhino.rs.HideGroup(self.group_edges)

    def _draw_edgelabels(self):
        """
        Draw labels for (some of) the edges of the diagram.
        This implementation is different than the base implementation for a normal mesh object,
        since the colors of the labels are different from the colors of the edges.

        Returns
        -------
        None

        """
        if not self.ui.registry["RV3"]["show.angles"]:
            return

        tol = self.ui.registry["RV3"]["tol.angles"]
        edges = list(self.diagram.edges_where(_is_edge=True))

        angles = self.diagram.edges_attribute("_a", keys=edges)
        amin = min(angles)
        amax = max(angles)
        aspan = amax - amin

        if aspan**2 < 0.001**2:
            return

        vertex_xyz = self.vertex_xyz

        labels = []
        for edge, angle in zip(edges, angles):
            if angle > tol:
                text = "{:.0f}".format(angle)
                color = Color.from_i((angle - amin) / aspan)

                labels.append(
                    {
                        "pos": centroid_points([vertex_xyz[edge[0]], vertex_xyz[edge[1]]]),
                        "name": "{}.edgelabel.{}-{}".format(self.diagram.name, *edge),
                        "color": color.rgb255,
                        "text": text,
                    }
                )
        guids = compas_rhino.draw_labels(labels, layer=self.settings["layer"], clear=False, redraw=False)
        self.guids += guids
