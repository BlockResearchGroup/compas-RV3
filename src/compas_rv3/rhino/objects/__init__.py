from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import plugin
from compas_ui.rhino.objects import RhinoObject
from compas_rv3.datastructures import Pattern

from .patternobject import RhinoPatternObject


@plugin(category="ui", requires=["Rhino"])
def register_objects():
    RhinoObject.register(Pattern, RhinoPatternObject, context="Rhino")

    print("RV3 Rhino Objects registered.")
