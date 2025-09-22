#!/usr/bin/env python3
"""
This module contains unit tests for the GithubOrgClient class.
It verifies that organization data is retrieved correctly without making
actual HTTP calls by mocking get_json.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license with different inputs"""
        from client import GithubOrgClient  # import inside to match style
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Start patcher for requests.get and configure side_effect"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # mock .json() return values depending on URL
        def side_effect(url):
            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            if url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            return MockResponse(None)

        class MockResponse:
            def __init__(self, payload):
                self._payload = payload
            def json(self):
                return self._payload

        mock_get.side_effect = side_effect

    def test_public_repos(self):
        """Integration test for public_repos without license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
