"""
module2.py – part of mypackage.subpackage
Demonstrates a module inside a sub-package (nested packages).
"""

def greet(name):
    """Return a greeting string."""
    return f"Hello from subpackage, {name}!"


def square(n):
    """Return the square of n."""
    return n ** 2


if __name__ == "__main__":
    print(greet("Mohammed"))   # Hello from subpackage, Mohammed!
    print(square(5))        # 25
