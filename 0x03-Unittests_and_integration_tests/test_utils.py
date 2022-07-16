#!/usr/bin/env python3
"""test utils for nested map function"""

from utils import access_nested_map
import unittest
from parameterized import parameterized


class TestAccessNestedMap(unittest.Testcase):
    """test utils for nested map function"""
    @parameterized.expand ([
        ({"a": 1}, ("a",)),
        ({"a": {"b": 2}}, ("a",)),
        ({"a": {"b": 2}}, ("a", "b"))

    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """test access_nested_map"""
        self.assertEqual(access_nested_map(nested_map, path), expected)


    