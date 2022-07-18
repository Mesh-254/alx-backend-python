#!/usr/bin/env python3
"""
a class to test the github_org_client.py file
"""
from typing import Any
import unittest
from client import GithubOrgClient
from unittest.mock import MagicMock, PropertyMock, patch
from parameterized import parameterized
from utils import get_json


class TestGithubOrgClient(unittest.TestCase):
    """
    a test to test the org function
    """

    @parameterized.expand([
        "google",
        "abc"
    ])
    @patch('client.GithubOrgClient.org')
    def test_org(self, name, mock_org):
        """
        a method to test org method
        """

        github_org_client = GithubOrgClient(name)
        github_org_client.org()
        mock_org.assert_called_once()

    def test_public_repos_url(self):
        """
        a method to test public_repos_url method
        """
        with patch('client.GithubOrgClient.org') as mock_org:
            mock_org.return_value = {
                "https://api.github.com/orgs/google/repos"
            }
            github_org_client = GithubOrgClient("google")
            self.assertEqual(github_org_client._public_repos_url,
                             "https://api.github.com/orgs/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_org: MagicMock) -> None:
        """
        a method to test public_repos method
        """
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos",
            "repos": [
                {
                    "name": "google",
                    "license": {
                        "key": "mit"
                    }
                },
                {
                    "name": "abc",
                    "license": {
                        "key": "mit"
                    }
                }
            ]
        }
        mock_org.return_value = test_payload["repos"]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock
                   ) as mock_org_repos:
            mock_org_repos.return_value = test_payload["repos_url"]
            github_org_client = GithubOrgClient("google")
            self.assertEqual(github_org_client.public_repos(),
                             ["google", "abc"])
            mock_org_repos.assert_called_once()
        mock_org.assert_called_once()

    @parameterized({
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    })
    def test_has_license(self, repo, license_key, expected_result):
        """
        a method to test has_license method
        """
        github_org_client = GithubOrgClient("google")
        self.assertTrue(github_org_client.has_license(repo, license_key))


if __name__ == '__main__':
    unittest.main()
