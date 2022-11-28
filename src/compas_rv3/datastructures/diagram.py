from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

# from compas.geometry import Point
# from compas.geometry import Line
# from compas.geometry import Polygon
from compas.datastructures import Mesh


class Diagram(Mesh):
    def __init__(self, *args, **kwargs):
        super(Diagram, self).__init__(*args, **kwargs)

    # def vertexpoint(self, vertex):
    #     return Point(*self.vertex_coordinates(vertex))

    # def edgeline(self, edge):
    #     return Line(self.vertex_coordinates(edge[0]), self.vertex_coordinates(edge[1]))

    # def facepolygon(self, face):
    #     return Polygon(self.face_coordinates(face))
