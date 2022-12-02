from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_tna.diagrams import FormDiagram
from compas_rv3.datastructures.diagram import Diagram


class FormDiagram(Diagram, FormDiagram):
    """
    Data structure for form diagrams.
    """

    @classmethod
    def from_pattern(cls, pattern):
        """Construct a form diagram from a pattern.

        Parameters
        ----------
        pattern : Pattern
            The pattern from which the diagram should be constructed.
        feet : {1, 2}, optional
            The number of horizontal force directions that should be added to the supports.

        Returns
        -------
        FormDiagram
            The form diagram.
        """
        form = pattern.copy(cls=cls)
        form.update_boundaries()
        return form
