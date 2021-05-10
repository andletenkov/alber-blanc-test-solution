"""
Module contains utility methods
"""
import random
import string


def random_string(length: int = 10) -> str:
    return ''.join([random.choice(string.ascii_letters) for _ in range(length)])
