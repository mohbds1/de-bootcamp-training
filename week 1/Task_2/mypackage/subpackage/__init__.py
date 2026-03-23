"""
mypackage/subpackage/__init__.py
This file marks 'subpackage' as a Python sub-package inside mypackage.
"""
from mypackage.subpackage.module2 import greet, square

__all__ = ["greet", "square"]
