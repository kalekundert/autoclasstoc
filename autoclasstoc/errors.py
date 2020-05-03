#!/usr/bin/env python3

class AutoClassTocError(Exception):
    pass

class ConfigError(AutoClassTocError):
    """
    Indicate an configuration error affecting :rst:dir:`autoclasstoc`.
    """
    pass


