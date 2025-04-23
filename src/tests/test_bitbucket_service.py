import unittest
from unittest.mock import patch, MagicMock
from src.services.bitbucket_service import BitbucketService

class TestBitbucketService(unittest.TestCase):

    @patch('src.services.bitbucket_service.requests.get')
    def test_get_team_data_success(self, mock_get):
        # Arrange
        mock_repos_response = MagicMock()
        mock_repos_response.json.return_value = {
            'values': [
                {'name': 'repo1', 'language': 'Python'},
                {'name': 'repo2', 'language': 'JavaScript', 'parent': {'name': 'repo1'}}
            ]
        }
        mock_team_response = MagicMock()
        mock_team_response.json.return_value = {'followers': 50}

        def side_effect(url):
            if 'repositories' in url:
                return mock_repos_response
            elif 'teams' in url:
                return mock_team_response

        mock_get.side_effect = side_effect

        service = BitbucketService('mailchimp')

        # Act
        result = service.get_team_data()

        # Assert
        self.assertEqual(result['public_repos']['total'], 2)
        self.assertEqual(result['public_repos']['original'], 1)
        self.assertEqual(result['public_repos']['forked'], 1)
        self.assertEqual(result['followers'], 50)
        self.assertIn('Python', result['languages'])
        self.assertIn('JavaScript', result['languages'])
        self.assertEqual(result['topics'], [])

    @patch('src.services.bitbucket_service.requests.get')
    def test_get_team_data_failure(self, mock_get):
        # Arrange
        mock_get.side_effect = Exception("Bitbucket API failure")

        service = BitbucketService('nonexistent_team')

        # Act
        result = service.get_team_data()

        # Assert
        self.assertEqual(result['error'], "Bitbucket API failure")

if __name__ == '__main__':
    unittest.main()