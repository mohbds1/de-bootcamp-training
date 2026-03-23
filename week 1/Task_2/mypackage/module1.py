"""
module1.py – part of mypackage
Demonstrates a simple module inside a package.
"""

def add(a, b):
    """Return the sum of a and b."""
    return a + b


def multiply(a, b):
    """Return the product of a and b."""
    return a * b


# Example constant
PI_APPROX = 3.14159

if __name__ == "__main__":
    print(add(3, 4))       # 7
    print(multiply(3, 4))  # 12
