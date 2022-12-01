from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import plugin
from compas_ui.rhino.objects import RhinoObject
from compas_rv3.datastructures import Pattern
from compas_rv3.datastructures import FormDiagram

from .patternobject import RhinoPatternObject
from .formobject import RhinoFormObject


@plugin(category="ui", requires=["Rhino"])
def register_objects():
    RhinoObject.register(Pattern, RhinoPatternObject, context="Rhino")
    RhinoObject.register(FormDiagram, RhinoFormObject, context="Rhino")

    print("RV3 Rhino Objects registered.")
