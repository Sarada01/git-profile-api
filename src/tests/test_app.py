import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Welcome to the Profile API!")

    def test_merge_profile(self):
        response = self.app.get('/api/profile?github_org=mailchimp&bitbucket_team=mailchimp')
        self.assertEqual(response.status_code, 200)
        response_json = response.get_json()
        self.assertIn('public_repos', response_json)
        self.assertIn('total', response_json['public_repos'])
        self.assertEqual(response_json['public_repos']['total'], 40)
        self.assertIn('languages', response_json)
        self.assertIn('topics', response_json)

    def test_merge_profile_missing_params(self):
        response = self.app.get('/api/profile')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())
        self.assertEqual(response.get_json()['error'], 'Both github_org and bitbucket_team are required')

    def test_merge_profile_invalid(self):
        response = self.app.get('/api/profile?github_org=invalid_org&bitbucket_team=invalid_team')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json(), {
            "error": "Failed to fetch data from GitHub or Bitbucket"
        })

if __name__ == '__main__':
    unittest.main()