#!/usr/bin/env python3
"""
:return the first element of a list or None if the list is empty
"""

from typing import Sequence, Any, Union


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """
    :return the first element of a list or None if the list is empty
    :param lst:
    :type lst:
    :return:
    :rtype:
    """
    if lst:
        return lst[0]
    else:
        return None
