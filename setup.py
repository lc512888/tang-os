"""Tang OS Reference Implementation — Setup for pip install.

Installation:
    pip install -e .           # development mode
    pip install tang-os        # future: from PyPI

Usage:
    from tang_os import Tang
    tang = Tang()
    result = tang.process("我今天很难过")
"""

from setuptools import setup

# Project metadata and package discovery are defined in pyproject.toml.
setup()
