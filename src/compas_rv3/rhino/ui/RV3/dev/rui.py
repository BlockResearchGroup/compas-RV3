import os
from compas_ui.rhino.rui import Rui

HERE = os.path.dirname(__file__)
UI = os.path.join(HERE, "ui.json")
RUI = os.path.join(HERE, "RV3.rui")

rui = Rui.from_json(UI, RUI)

rui.write()
