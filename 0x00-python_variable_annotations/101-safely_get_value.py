#!/usr/bin/env python3
"""
:return: a dictionary with the following keys:
"""
from typing import Mapping, Any, Union, TypeVar

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """
    :param dct: a dictionary
    :param dct:
    :type dct:
    :param key:
    :type key:
    :param default:
    :type default:
    :return:
    :rtype:
    """
    if key in dct:
        return dct[key]
    else:
        return default
