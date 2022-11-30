from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_ui.objects import MeshObject


class DiagramObject(MeshObject):
    """Scene object for RV2 form/force diagrams."""

    @property
    def diagram(self):
        return self.item

    @diagram.setter
    def diagram(self, diagram):
        self.item = diagram
