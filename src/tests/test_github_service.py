import unittest
from unittest.mock import patch, MagicMock
from services.github_service import GitHubService

class TestGitHubService(unittest.TestCase):

    @patch('services.github_service.requests.get')
    def test_get_organization_data(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'public_repos': 10,
            'followers': 100,
            'languages': ['Python', 'JavaScript'],
            'forked_repos': 5,
            'watchers': 50,
            'topics': ['api', 'flask', 'python']
        }
        mock_get.return_value = mock_response

        service = GitHubService()
        
        # Act
        data = service.get_organization_data('mailchimp')

        # Assert
        self.assertEqual(data['public_repos'], 10)
        self.assertEqual(data['followers'], 100)
        self.assertEqual(data['languages'], ['Python', 'JavaScript'])
        self.assertEqual(data['forked_repos'], 5)
        self.assertEqual(data['watchers'], 50)
        self.assertEqual(data['topics'], ['api', 'flask', 'python'])

    @patch('services.github_service.requests.get')
    def test_get_organization_data_no_repos(self, mock_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'public_repos': 0,
            'followers': 0,
            'languages': [],
            'forked_repos': 0,
            'watchers': 0,
            'topics': []
        }
        mock_get.return_value = mock_response

        service = GitHubService()
        
        # Act
        data = service.get_organization_data('nonexistent_org')

        # Assert
        self.assertEqual(data['public_repos'], 0)
        self.assertEqual(data['followers'], 0)
        self.assertEqual(data['languages'], [])
        self.assertEqual(data['forked_repos'], 0)
        self.assertEqual(data['watchers'], 0)
        self.assertEqual(data['topics'], [])

if __name__ == '__main__':
    unittest.main()