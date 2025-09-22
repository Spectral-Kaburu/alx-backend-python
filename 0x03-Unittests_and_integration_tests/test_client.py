#!/usr/bin/env python3
"""
This module contains unit tests for the GithubOrgClient class.
It verifies that organization data is retrieved correctly without making
actual HTTP calls by mocking get_json.
"""

import unittest
from unittest.mock import patch, PropertyMock
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

    def test_public_repos_url(self) -> None:
        """
        Test that GithubOrgClient._public_repos_url returns the repos_url
        from the mocked org payload.
        """
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        client = GithubOrgClient("test")

        with patch.object(GithubOrgClient, "org", new_callable=property) as m:
            m.return_value = test_payload
            result = client._public_repos_url

        self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "http://fake-url.com"

            client = GithubOrgClient("test_org")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake-url.com")


if __name__ == "__main__":
    unittest.main()
