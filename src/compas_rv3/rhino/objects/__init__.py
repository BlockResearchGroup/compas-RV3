from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.plugins import plugin
from compas_ui.rhino.objects import RhinoObject
from compas_rv3.datastructures import Pattern
from compas_rv3.datastructures import FormDiagram
from compas_rv3.datastructures import ForceDiagram
from compas_rv3.datastructures import ThrustDiagram

from .patternobject import RhinoPatternObject
from .formobject import RhinoFormObject
from .forceobject import RhinoForceObject
from .thrustobject import RhinoThrustObject


@plugin(category="ui", requires=["Rhino"])
def register_objects():
    RhinoObject.register(Pattern, RhinoPatternObject, context="Rhino")
    RhinoObject.register(FormDiagram, RhinoFormObject, context="Rhino")
    RhinoObject.register(ForceDiagram, RhinoForceObject, context="Rhino")
    RhinoObject.register(ThrustDiagram, RhinoThrustObject, context="Rhino")

    print("RV3 Rhino Objects registered.")
