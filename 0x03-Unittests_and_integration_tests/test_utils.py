#!/usr/bin/env python3
"""
This module contains unit tests for the utils.access_nested_map function.
It ensures that nested dictionary access works correctly for given paths.
"""

import unittest
from parameterized import parameterized
from typing import Any, Mapping, Sequence
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """
    TestAccessNestedMap defines unit tests for the access_nested_map function.
    It verifies that values can be retrieved correctly from nested mappings.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
        expected: Any
    ) -> None:
        """
        Test that access_nested_map returns the expected value for given inputs.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
    ) -> None:
        """
        Test that access_nested_map raises KeyError with the correct message
        when a key in the path is missing.
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), repr(path[-1]))

if __name__ == "__main__":
    unittest.main()
