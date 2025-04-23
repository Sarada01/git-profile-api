from flask import current_app
import requests

class GitHubService:
    BASE_URL = "https://api.github.com"

    def __init__(self, org_name):
        self.org_name = org_name

    def get_organization_data(self):
        try:
            org_data = self._fetch_organization_data()
            repos_data = self._fetch_repositories_data()
            
            return {
                "public_repos": {
                    "total": len(repos_data),
                    "original": len([repo for repo in repos_data if not repo.get('fork')]),
                    "forked": len([repo for repo in repos_data if repo.get('fork')]),
                },
                "followers": org_data.get('followers', 0),
                "languages": self._get_languages_used(repos_data),
                "topics": self._get_repo_topics(repos_data),
            }
        except Exception as e:
            return {"error": str(e)}

    def _fetch_organization_data(self):
        url = f"{self.BASE_URL}/orgs/{self.org_name}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _fetch_repositories_data(self):
        url = f"{self.BASE_URL}/orgs/{self.org_name}/repos"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def _get_languages_used(self, repos_data):
        languages = set()
        for repo in repos_data:
            if repo.get('language'):  # Check if the 'language' field exists
                languages.add(repo['language'])
        return list(languages)

    def _get_repo_topics(self, repos_data):
        topics = set()
        for repo in repos_data:
            topics_url = f"{self.BASE_URL}/repos/{self.org_name}/{repo['name']}/topics"
            headers = {'Accept': 'application/vnd.github.mercy-preview+json'}
            topics_response = requests.get(topics_url, headers=headers)
            if topics_response.status_code == 200:
                topics.update(topics_response.json().get('names', []))
        return list(topics)