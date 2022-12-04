from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas.colors import Color
from compas.geometry import centroid_points
from compas.utilities import remap_values

from compas_rv3.objects import FormObject
from .diagramobject import RhinoDiagramObject


class RhinoFormObject(RhinoDiagramObject, FormObject):
    """
    Rhino scene object for form diagrams in RV3.
    """

    def __init__(self, *args, **kwargs):
        super(RhinoFormObject, self).__init__(*args, **kwargs)
        self.add_group(self.groupname_vertices_free)
        self.add_group(self.groupname_vertices_anchored)

    @property
    def groupname_vertices_free(self):
        return "{}::vertices::free".format(self.settings["layer"])

    @property
    def groupname_vertices_anchored(self):
        return "{}::vertices::anchored".format(self.settings["layer"])

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
        free = list(self.diagram.vertices_where(is_anchor=False))
        fixed = list(self.diagram.vertices_where(is_fixed=True))
        anchored = list(self.diagram.vertices_where(is_anchor=True))

        color = {}
        color_free = self.settings["color.vertices"]
        color_fixed = self.settings["color.vertices:is_fixed"]
        color_anchor = self.settings["color.vertices:is_anchor"]
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
        color = self.settings["color.edges"]
        edge_color = {edge: color for edge in edges}

        if self.ui.registry["RV3"]["show.forces"]:
            if self.diagram.dual:
                _edges = list(self.diagram.dual.edges())
                edges = [self.diagram.dual.primal_edge(edge) for edge in _edges]
                lengths = [self.diagram.dual.edge_length(*edge) for edge in _edges]
                for edge, value in zip(edges, remap_values(lengths)):
                    edge_color[edge] = Color.from_i(value)

        guids = self.artist.draw_edges(edges, edge_color)
        self.guids += guids
        self.guid_edge = zip(guids, edges)

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
