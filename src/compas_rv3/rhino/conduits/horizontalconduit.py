from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino.conduits import BaseConduit

from Rhino.Geometry import Point3d
from Rhino.Geometry import Line

from System.Collections.Generic import List
from System.Drawing.Color import FromArgb


class HorizontalConduit(BaseConduit):
    """A Rhino display conduit for lines.

    Parameters
    ----------
    lines : list of 2-tuple
        A list of start-end point pairs that define the lines.
    thickness : list of int, optional
        The thickness of the individual lines.
        Default is ``1.0`` for all lines.
    color : list of str or 3-tuple, optional
        The colors of the faces.
        Default is ``(255, 255, 255)`` for all lines.

    Attributes
    ----------
    color
    thickness
    lines : list
        A list of start-end point pairs that define the lines.

    Examples
    --------
    >>>

    """

    def __init__(self, lines, **kwargs):
        super(HorizontalConduit, self).__init__(**kwargs)
        self._default_thickness = 1.0
        self._default_color = FromArgb(255, 255, 255)
        self.lines = lines or []

    def DrawForeground(self, e):
        lines = List[Line](len(self.lines))
        for start, end in self.lines:
            lines.Add(Line(Point3d(start[0], start[1], 0), Point3d(end[0], end[1], 0)))
        e.Display.DrawLines(lines, self._default_color, self._default_thickness)
