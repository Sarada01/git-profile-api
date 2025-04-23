from flask import current_app
import requests

class GitHubService:
    BASE_URL = "https://api.github.com"  # Base URL for GitHub API

    def __init__(self, org_name):
        self.org_name = org_name  # Initialize with the organization name

    def get_organization_data(self):
        """
        Fetches data for the specified GitHub organization, including repository counts,
        followers, languages used, and topics.
        """
        try:
            # Fetch organization and repository data
            org_data = self._fetch_organization_data()
            repos_data = self._fetch_repositories_data()
            
            return {
                "public_repos": {
                    "total": len(repos_data),  # Total repositories
                    "original": len([repo for repo in repos_data if not repo.get('fork')]),  # Original repos
                    "forked": len([repo for repo in repos_data if repo.get('fork')]),  # Forked repos
                },
                "followers": org_data.get('followers', 0),  # Number of followers
                "languages": self._get_languages_used(repos_data),  # Languages used
                "topics": self._get_repo_topics(repos_data),  # Topics associated with repos
            }
        except Exception as e:
            # Return error message in case of failure
            return {"error": str(e)}

    def _fetch_organization_data(self):
        """
        Fetches metadata for the organization from the GitHub API.
        """
        url = f"{self.BASE_URL}/orgs/{self.org_name}"  # Construct the URL
        response = requests.get(url)  # Perform the GET request
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response

    def _fetch_repositories_data(self):
        """
        Fetches repository data for the organization from the GitHub API.
        """
        url = f"{self.BASE_URL}/orgs/{self.org_name}/repos"  # Construct the URL
        response = requests.get(url)  # Perform the GET request
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response

    def _get_languages_used(self, repos_data):
        """
        Extracts the set of programming languages used in the repositories.
        """
        languages = set()
        for repo in repos_data:
            if repo.get('language'):  # Check if the 'language' field exists
                languages.add(repo['language'])
        return list(languages)  # Convert set to list for JSON serialization

    def _get_repo_topics(self, repos_data):
        """
        Fetches and aggregates topics for all repositories in the organization.
        """
        topics = set()
        for repo in repos_data:
            topics_url = f"{self.BASE_URL}/repos/{self.org_name}/{repo['name']}/topics"  # Construct the URL
            headers = {'Accept': 'application/vnd.github.mercy-preview+json'}  # Use preview API for topics
            topics_response = requests.get(topics_url, headers=headers)  # Perform the GET request
            if topics_response.status_code == 200:  # Check for successful response
                topics.update(topics_response.json().get('names', []))  # Add topics to the set
        return list(topics)  # Convert set to list for JSON serialization