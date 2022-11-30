from compas_ui.ui import UI


def get_object_by_name(name, message="There is no {} in the scene."):
    ui = UI()
    objects = ui.scene.get(name)
    if not objects:
        raise RuntimeError(message.format(name))
    return objects[0]
