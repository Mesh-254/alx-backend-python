#!/usr/bin/env python3
"""
Convert a key-value pair to a key-value pair.
"""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """
    Convert a key-value pair to a key-value pair.
    :param k:
    :type k:
    :param v:
    :type v:
    :return:
    :rtype:
    """
    return k, v ** 2
