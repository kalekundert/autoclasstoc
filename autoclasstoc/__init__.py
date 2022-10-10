#!/usr/bin/env python3

"""\
Add a succinct TOC to auto-documented classes.
"""

__version__ = '1.5.2'

from .errors import *
from . import utils, nodes
from .sections import *
from .plugin import *

# Make this package appear flat to external tools (e.g. sphinx):
from inspect import isfunction, isclass

for obj in locals().copy().values():
    if isfunction(obj) or isclass(obj):
        obj.__module__ = 'autoclasstoc'

del inspect, isfunction, isclass, obj
