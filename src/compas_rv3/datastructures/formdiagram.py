from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rv3.datastructures.diagram import Diagram


class FormDiagram(Diagram):
    def __init__(self, *args, **kwargs):
        super(FormDiagram, self).__init__(*args, **kwargs)