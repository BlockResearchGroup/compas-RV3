from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
from compas_ui.ui import UI
from compas_ui.rhino.forms import ToolbarForm


__commandname__ = "RV3_toolbar"


HERE = os.path.dirname(__file__)


@UI.error()
def RunCommand(is_interactive):

    ui = UI()  # noqa: F841

    config = [
        {
            "command": "RV3_toolbar_pattern",
            "icon": os.path.join(HERE, "assets", "RV3_pattern.png"),
        },
        {
            "command": "RV3_toolbar_modify_pattern",
            "icon": os.path.join(HERE, "assets", "RV3_modify_pattern.png"),
        },
        {
            "command": "RV3_toolbar_boundary",
            "icon": os.path.join(HERE, "assets", "RV3_boundary.png"),
        },
        {"type": "separator"},
        {
            "command": "RV3_form",
            "icon": os.path.join(HERE, "assets", "RV3_form.png"),
        },
        {
            "command": "RV3_force",
            "icon": os.path.join(HERE, "assets", "RV3_force.png"),
        },
        {"type": "separator"},
        {
            "command": "RV3_tna_horizontal",
            "icon": os.path.join(HERE, "assets", "RV3_tna_horizontal.png"),
        },
        {
            "command": "RV3_tna_vertical",
            "icon": os.path.join(HERE, "assets", "RV3_tna_vertical.png"),
        },
        {"type": "separator"},
        {
            "command": "RV3_toolbar_modify_form",
            "icon": os.path.join(HERE, "assets", "RV3_modify_form.png"),
        },
        {
            "command": "RV3_toolbar_modify_force",
            "icon": os.path.join(HERE, "assets", "RV3_modify_force.png"),
        },
        {
            "command": "RV3_toolbar_modify_thrust",
            "icon": os.path.join(HERE, "assets", "RV3_modify_thrust.png"),
        },
    ]

    toolbar = ToolbarForm()
    toolbar.setup(config, HERE, title="RhinoVAULT 3")
    toolbar.Show()


if __name__ == "__main__":
    RunCommand(True)
