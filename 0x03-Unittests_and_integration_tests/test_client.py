#!/usr/bin/env python3
"""Unit tests for client module."""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests with fixtures for GithubOrgClient."""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and setup mock return values."""
        cls.get_patcher = patch('client.requests.get')
        mock_get = cls.get_patcher.start()

        # Set side_effect based on URL
        def side_effect(url):
            if url.endswith('/orgs/google'):
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.org_payload
                return mock_response
            elif url.endswith('/orgs/google/repos'):
                mock_response = unittest.mock.Mock()
                mock_response.json.return_value = cls.repos_payload
                return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos method."""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filtering."""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"), self.apache2_repos)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected result."""
        payload = {'login': org_name}
        mock_get_json.return_value = payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test _public_repos_url property."""
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {'repos_url': 'http://some_url'}
            client = GithubOrgClient('google')
            self.assertEqual(client._public_repos_url, 'http://some_url')

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method."""
        mock_get_json.return_value = [
            {'name': 'repo1'},
            {'name': 'repo2'},
            {'name': 'repo3'}
        ]
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_url:
            mock_url.return_value = 'http://some_url'
            client = GithubOrgClient('google')
            result = client.public_repos()
            self.assertEqual(result, ['repo1', 'repo2', 'repo3'])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with('http://some_url')

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
