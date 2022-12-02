from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Mesh
from compas.datastructures import mesh_smooth_area
from compas.geometry import angle_vectors


class Diagram(Mesh):
    def __init__(self, *args, **kwargs):
        super(Diagram, self).__init__(*args, **kwargs)

    def edge_loop(self, uv):
        if self.is_edge_on_boundary(*uv):
            return self._edge_loop_on_boundary(uv)

        edges = []
        current, previous = uv
        edges.append((previous, current))

        while True:
            if current == uv[1]:
                break
            if self.vertex_attribute(current, "is_fixed"):
                break
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            edges.append((previous, current))

        edges[:] = [(u, v) for v, u in edges[::-1]]

        if edges[0][0] == edges[-1][1]:
            return edges

        previous, current = uv
        while True:
            if self.vertex_attribute(current, "is_fixed"):
                break
            nbrs = self.vertex_neighbors(current, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(previous)
            previous = current
            current = nbrs[i - 2]
            edges.append((previous, current))

        return edges

    def _edge_loop_on_boundary(self, uv):
        edges = []
        current, previous = uv
        edges.append((previous, current))

        while True:
            if current == uv[1]:
                break
            if self.vertex_attribute(current, "is_fixed"):
                break
            nbrs = self.vertex_neighbors(current)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == previous:
                    continue
                if self.is_edge_on_boundary(current, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            previous, current = current, nbr
            edges.append((previous, current))

        edges[:] = [(u, v) for v, u in edges[::-1]]

        if edges[0][0] == edges[-1][1]:
            return edges

        previous, current = uv
        while True:
            if self.vertex_attribute(current, "is_fixed"):
                break
            nbrs = self.vertex_neighbors(current)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == previous:
                    continue
                if self.is_edge_on_boundary(current, temp):
                    nbr = temp
                    break
            if nbr is None:
                break
            previous, current = current, nbr
            edges.append((previous, current))

        return edges

    def collapse_small_edges(self, tol=1e-2):
        """
        Collapse the edges that are shorter than a given length.

        Parameters
        ----------
        tol : float, optional
            The threshold length.
            Edges with a length shorter than this value
            will be collapsed.

        Returns
        -------
        None

        """
        for key in list(self.edges()):
            if self.has_edge(key):
                u, v = key
                if self.edge_length(u, v) < tol:
                    self.collapse_edge(u, v, t=0.5, allow_boundary=True)

    def smooth(self, fixed, kmax=10):
        """
        Apply area smoothing to the mesh geometry.

        Parameters
        ----------
        fixed : list[int]
            The vertices to keep fixed.
        kmax : int, optional
            The number of smoothing iterations.

        Returns
        -------
        None

        """
        mesh_smooth_area(self, fixed=fixed, kmax=kmax)

    def relax(self):
        """
        Relax the mesh using the force density method with the curent edge force densities.

        Returns
        -------
        None

        """
        from compas.numerical import fd_numpy

        key_index = self.key_index()
        xyz = self.vertices_attributes("xyz")
        loads = [[0.0, 0.0, 0.0] for _ in xyz]
        fixed = [key_index[key] for key in self.vertices_where({"is_fixed": True})]
        edges = [(key_index[u], key_index[v]) for u, v in self.edges()]
        q = self.edges_attribute("q")
        xyz, q, f, l, r = fd_numpy(xyz, edges, fixed, q, loads)
        for key in self.vertices():
            index = key_index[key]
            self.vertex_attributes(key, "xyz", xyz[index])

    def corner_vertices(self, tol=160):
        """
        Identify the corner vertices.

        Parameters
        ----------
        tol : float, optional
            The threshold value for the angle formed between two edges at a vertex
            for it to be considered a corner.
            Vertices with smaller angles are considered a corner.

        Returns
        -------
        list[int]

        """
        vkeys = []
        for key in self.vertices_on_boundary():
            if self.vertex_degree(key) == 2:
                vkeys.append(key)
            else:
                nbrs = []
                for nkey in self.vertex_neighbors(key):
                    if self.is_edge_on_boundary(key, nkey):
                        nbrs.append(nkey)
                u = self.edge_vector(key, nbrs[0])
                v = self.edge_vector(key, nbrs[1])
                if angle_vectors(u, v, deg=True) < tol:
                    vkeys.append(key)
        return vkeys

    def edge_loop_vertices(self, uv):
        """
        Identify all vertices on an edge loop.

        Parameters
        ----------
        uv : tuple[int, int]
            The identifier of the base edge of the loop.

        Returns
        -------
        list[int]

        """
        edges = self.edge_loop(uv)
        if len(edges) == 1:
            return edges[0]
        vertices = [edge[0] for edge in edges]
        if edges[-1][1] != edges[0][0]:
            vertices.append(edges[-1][1])
        return vertices
