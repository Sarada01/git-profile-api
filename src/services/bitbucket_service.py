class BitbucketService:
    BASE_URL = "https://api.bitbucket.org/2.0"  # Base URL for Bitbucket API

    def __init__(self, team_name):
        self.team_name = team_name  # Initialize with the team name

    def get_team_data(self):
        """
        Fetches data for the specified Bitbucket team, including repository counts,
        languages used, and other metadata.
        """
        try:
            # Fetch repositories for the team
            repos = self._make_request(f"/repositories/{self.team_name}")
            return {
                "public_repos": {
                    "total": len(repos.get("values", [])),  # Total repositories
                    "original": len([repo for repo in repos.get("values", []) if repo["parent"] == None]),  # Original repos
                    "forked": len([repo for repo in repos.get("values", []) if repo["parent"] != None]),  # Forked repos
                },
                "followers": 0,  # Placeholder for followers (not provided by Bitbucket API)
                "languages": self._get_languages_used(repos),  # Languages used in repositories
                "topics": [],  # Placeholder for topics (not provided by Bitbucket API)
            }
        except Exception as e:
            # Return error message in case of failure
            return {"error": str(e)}

    def _get_languages_used(self, repos):
        """
        Extracts the set of programming languages used in the repositories.
        """
        languages = set()
        for repo in repos.get("values", []):
            if "language" in repo:  # Check if the 'language' field exists
                languages.add(repo["language"])
        return list(languages)  # Convert set to list for JSON serialization

    def _make_request(self, endpoint):
        """
        Makes a GET request to the specified Bitbucket API endpoint.
        """
        import requests
        url = f"{self.BASE_URL}{endpoint}"  # Construct the full URL
        response = requests.get(url)  # Perform the GET request
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Return the JSON response