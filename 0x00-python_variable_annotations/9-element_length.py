#!/usr/bin/env python3
"""
:return a list of tuples with the element and its length
"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """
    :param lst: a list of sequences
    :param lst:
    :type lst:
    :return:
    :rtype:
    """
    return [(i, len(i)) for i in lst]
