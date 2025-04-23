import unittest
from unittest.mock import patch, MagicMock
from src.controllers.profile_controller import ProfileController

class TestProfileController(unittest.TestCase):

    @patch('src.controllers.profile_controller.GitHubService')
    @patch('src.controllers.profile_controller.BitbucketService')
    def test_merge_profiles_success(self, mock_bitbucket_service, mock_github_service):
        # Arrange
        mock_github_service_instance = mock_github_service.return_value
        mock_bitbucket_service_instance = mock_bitbucket_service.return_value
        
        mock_github_service_instance.get_organization_data.return_value = {
            'public_repos': 10,
            'forked_repos': 2,
            'watchers': 100,
            'languages': ['Python', 'JavaScript'],
            'topics': ['API', 'Web']
        }
        
        mock_bitbucket_service_instance.get_team_data.return_value = {
            'public_repos': 5,
            'followers': 50,
            'languages': ['Python', 'Java'],
            'topics': ['Development', 'Open Source']
        }
        
        controller = ProfileController(mock_github_service_instance, mock_bitbucket_service_instance)

        # Act
        result = controller.merge_profiles('mailchimp', 'mailchimp')

        # Assert
        self.assertEqual(result['total_public_repos'], 15)
        self.assertEqual(result['total_forked_repos'], 2)
        self.assertEqual(result['total_watchers'], 100)
        self.assertEqual(result['total_followers'], 50)
        self.assertEqual(set(result['languages']), {'Python', 'JavaScript', 'Java'})
        self.assertEqual(set(result['topics']), {'API', 'Web', 'Development', 'Open Source'})

    @patch('src.controllers.profile_controller.GitHubService')
    @patch('src.controllers.profile_controller.BitbucketService')
    def test_merge_profiles_github_failure(self, mock_bitbucket_service, mock_github_service):
        # Arrange
        mock_github_service_instance = mock_github_service.return_value
        mock_bitbucket_service_instance = mock_bitbucket_service.return_value
        
        mock_github_service_instance.get_organization_data.side_effect = Exception("GitHub API failure")
        mock_bitbucket_service_instance.get_team_data.return_value = {
            'public_repos': 5,
            'followers': 50,
            'languages': ['Python'],
            'topics': ['Development']
        }
        
        controller = ProfileController(mock_github_service_instance, mock_bitbucket_service_instance)

        # Act
        result = controller.merge_profiles('mailchimp', 'mailchimp')

        # Assert
        self.assertEqual(result['error'], "GitHub API failure")
        self.assertEqual(result['total_public_repos'], 5)
        self.assertEqual(result['total_followers'], 50)

if __name__ == '__main__':
    unittest.main()