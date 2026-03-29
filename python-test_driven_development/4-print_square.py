#!/usr/bin/python3
"""
3. Print square
"""


def print_square(size):
    """
    Prints a square with the character #.
    size must be an integer >= 0.
    """
    if isinstance(size, float):
        raise TypeError("size must be an integer")
    if not isinstance(size, int):
        raise TypeError("size must be an integer")
    if size < 0:
        raise ValueError("size must be >= 0")
    for _ in range(size):
        print("#" * size)
