"""
mypackage/__init__.py
This file marks 'mypackage' as a Python package.
You can optionally expose symbols here for convenience.
"""

# Make key functions available at the package level
from mypackage.module1 import add, multiply

__all__ = ["add", "multiply"]
