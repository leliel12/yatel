
from __future__ import absolute_import

import os

from yatelui import resdir


PATH = os.path.abspath(os.path.dirname(__file__)) + os.path.sep

RESOURCES = resdir.ResourceDirs(PATH, "ui")

for k in dir(RESOURCES):
    if not k.startswith("_"):
        v = getattr(RESOURCES, k)
        globals()[k] = v
    

