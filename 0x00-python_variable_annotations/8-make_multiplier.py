#!/usr/bin/env python3
"""
:return a function that multiplies its argument by a given multiplier
"""

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """
    :param multiplier: a multiplier
    :param multiplier:
    :type multiplier:
    :return:
    :rtype:
    """

    def multiply(x: float) -> float:
        """
        multiply the given number by the multiplier
        :param x:
        :type x:
        :return:
        :rtype:
        """
        return x * multiplier

    return multiply
