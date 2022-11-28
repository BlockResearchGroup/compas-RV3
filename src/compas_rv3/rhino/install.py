from compas.plugins import plugin


@plugin(category="install", tryfirst=True)
def installable_rhino_packages():
    return ["compas_rv2"]


if __name__ == "__main__":

    print("This installation procedure is deprecated.")
    print("Use `python -m compas_rhino.install` instead.")