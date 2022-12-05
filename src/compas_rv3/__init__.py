"""
********************************************************************************
compas_rv3
********************************************************************************

.. currentmodule:: compas_rv3


.. toctree::
    :maxdepth: 1


"""

from __future__ import print_function

import os


__author__ = ["Tom Van Mele, Juney Lee, Li Chen"]
__copyright__ = "ETH Zurich - Block Research Group"
__license__ = "MIT License"
__email__ = "van.mele@arch.ethz.ch, juney-lee@som.com, li.chen@arch.ethz.ch"
__version__ = "0.3.0"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))


__all__ = ["HOME", "DATA", "DOCS", "TEMP"]

__all_plugins__ = [
    "compas_rv3.rhino.install",
    "compas_rv3.rhino.register",
    "compas_rv3.rhino.artists",
    "compas_rv3.rhino.objects",
]
