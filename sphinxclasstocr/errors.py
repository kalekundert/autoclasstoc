#!/usr/bin/env python3


class SphinxClassTocrError(Exception):

    """Base exception for sphinxclasstocr"""

    pass


class ConfigError(SphinxClassTocrError):

    """Raise a configuration error for :rst:dir:`sphinxclasstocr`."""
