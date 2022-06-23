#!/usr/bin/env python3
"""
:return sum of mixed list
"""

from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """
    sum the elements of a mixed list.
    """
    return sum(mxd_lst)
