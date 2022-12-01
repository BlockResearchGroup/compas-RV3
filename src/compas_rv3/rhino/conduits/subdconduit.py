from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas_rhino.conduits import BaseConduit

from System.Drawing.Color import FromArgb

from Rhino.Geometry import Point3d


class SubdConduit(BaseConduit):
    """Display conduit for subdmesh.

    Parameters
    ----------
    lines : list of two tuples
        List of pairs of coordinates.
    thickness : float
        Thickness of the lines.
    color : tuple
        Color of the lines.
    """

    def __init__(self, lines, thickness=1.0, color=(125, 125, 125), **kwargs):
        super(SubdConduit, self).__init__(**kwargs)
        self.lines = lines or []
        self.thickness = thickness
        self.color = color

    def DrawForeground(self, e):
        for line in self.lines:
            sp = line[0]
            ep = line[1]
            color = self.color
            e.Display.DrawLine(Point3d(*sp),
                               Point3d(*ep),
                               FromArgb(*color),
                               self.thickness)
