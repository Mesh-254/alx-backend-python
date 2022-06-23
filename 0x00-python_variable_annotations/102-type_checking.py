#!/usr/bin/env python3
"""
:return zoomed_in: a list of items in lst, repeated factor times
"""
from typing import Tuple, List, Any


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    """
    :param lst: a list of items
    :param lst:
    :type lst:
    :param factor:
    :type factor:
    :return:
    :rtype:
    """
    zoomed_in: List[Any] = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array: Tuple = tuple([12, 72, 91])

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
