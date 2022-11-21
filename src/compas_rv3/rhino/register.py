import os
from compas.plugins import plugin

from compas_ui.values import Settings
# from compas_ui.values import BoolValue
# from compas_ui.values import FloatValue

HERE = os.path.dirname(__file__)

SETTINGS = Settings({})


@plugin(category="ui")
def register(ui):

    plugin_name = "RV3"
    plugin_path = os.path.join(HERE, "ui", plugin_name)
    if not os.path.isdir(plugin_path):
        raise Exception("Cannot find the plugin: {}".format(plugin_path))

    ui.registry["RV3"] = SETTINGS


# @plugin(category="ui")
# def pre_undo(ui):
#     pass


# @plugin(category="ui")
# def post_undo(ui):
#     pairs = {}

#     for obj in ui.scene.objects:
#         name = obj.name
#         if name.startswith("FormDiagram"):
#             if name == "FormDiagram":
#                 index = 0
#             else:
#                 index = int(name.split(".")[-1]) + 1
#             if index not in pairs:
#                 pairs[index] = {"form": None, "force": None}
#             pairs[index]["form"] = obj

#     for obj in ui.scene.objects:
#         name = obj.name
#         if name.startswith("ForceDiagram"):
#             if name == "ForceDiagram":
#                 index = 0
#             else:
#                 index = int(name.split(".")[-1]) + 1
#             if index not in pairs:
#                 pairs[index] = {"form": None, "force": None}
#             pairs[index]["force"] = obj

#     for index in pairs:
#         form = pairs[index]["form"]
#         force = pairs[index]["force"]
#         if form:
#             if force:
#                 form.diagram.dual = force.diagram
#         if force:
#             if form:
#                 force.diagram.dual = form.diagram


# @plugin(category="ui")
# def pre_redo(ui):
#     pass


# @plugin(category="ui")
# def post_redo(ui):
#     pairs = {}

#     for obj in ui.scene.objects:
#         name = obj.name
#         if name.startswith("FormDiagram"):
#             if name == "FormDiagram":
#                 index = 0
#             else:
#                 index = int(name.split(".")[-1]) + 1
#             if index not in pairs:
#                 pairs[index] = {"form": None, "force": None}
#             pairs[index]["form"] = obj

#     for obj in ui.scene.objects:
#         name = obj.name
#         if name.startswith("ForceDiagram"):
#             if name == "ForceDiagram":
#                 index = 0
#             else:
#                 index = int(name.split(".")[-1]) + 1
#             if index not in pairs:
#                 pairs[index] = {"form": None, "force": None}
#             pairs[index]["force"] = obj

#     for index in pairs:
#         form = pairs[index]["form"]
#         force = pairs[index]["force"]
#         if form:
#             if force:
#                 form.diagram.dual = force.diagram
#         if force:
#             if form:
#                 force.diagram.dual = form.diagram
