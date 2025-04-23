import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_merge_profile(self):
        response = self.app.post('/merge-profile', json={
            'github_org': 'mailchimp',
            'bitbucket_team': 'mailchimp'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_repos', response.get_json())
        self.assertIn('languages', response.get_json())
        self.assertIn('topics', response.get_json())

    def test_merge_profile_invalid(self):
        response = self.app.post('/merge-profile', json={
            'github_org': 'invalid_org',
            'bitbucket_team': 'invalid_team'
        })
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()