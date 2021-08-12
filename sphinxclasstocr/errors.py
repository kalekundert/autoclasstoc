#!/usr/bin/env python3


class SphinxClassTocrError(Exception):
    pass


class ConfigError(SphinxClassTocrError):
    """
    Indicate an configuration error affecting :rst:dir:`sphinxclasstocr`.
    """

    pass
