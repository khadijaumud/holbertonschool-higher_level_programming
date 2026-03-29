#!/usr/bin/python3
"""
4. Text indentation
"""


def text_indentation(text):
    """
    Prints text with 2 new lines after each '.', '?' and ':'.
    No spaces at the beginning or end of each printed line.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    i = 0
    while i < len(text):
        print(text[i], end="")
        if text[i] in ".?:":
            print("\n")
            i += 1
            while i < len(text) and text[i] == " ":
                i += 1
            continue
        i += 1
