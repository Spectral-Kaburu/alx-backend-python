#!/usr/bin/env python3
"""
This module contains unit tests for the GithubOrgClient class.
It verifies that organization data is retrieved correctly without making
actual HTTP calls by mocking get_json.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from typing import Dict
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient defines unit tests for the GithubOrgClient class.
    It ensures that organization data is fetched correctly via get_json.
    """

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch("client.get_json")
    def test_org(
        self,
        org_name: str,
        expected_return: Dict,
        mock_get_json
    ) -> None:
        """
        Test that GithubOrgClient.org returns the mocked organization payload
        and that get_json is called once with the correct URL.
        """
        mock_get_json.return_value = expected_return
        client = GithubOrgClient(org_name)

        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_return)


if __name__ == "__main__":
    unittest.main()
