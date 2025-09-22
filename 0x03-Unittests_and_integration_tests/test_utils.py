#!/usr/bin/env python3
"""
This module contains unit tests for the utils.access_nested_map function.
It ensures that nested dictionary access works correctly for given paths.
"""

import unittest
from parameterized import parameterized
from typing import Any, Mapping, Sequence, Dict
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


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


class TestGetJson(unittest.TestCase):
    """
    TestGetJson defines unit tests for the get_json function.
    It verifies that JSON payloads are returned as expected from mocked URLs.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict[str, Any]) -> None:
        """
        Test that get_json returns the expected JSON payload and that
        requests.get is called exactly once with the correct URL.
        """
        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

if __name__ == "__main__":
    unittest.main()
