class BitbucketService:
    BASE_URL = "https://api.bitbucket.org/2.0"

    def __init__(self, team_name):
        self.team_name = team_name

    def get_team_data(self):
        try:
            repos = self._make_request(f"/repositories/{self.team_name}")
            return {
                "public_repos": {
                    "total": len(repos.get("values", [])),
                    "original": len([repo for repo in repos.get("values", []) if repo["parent"] ==None]),
                    "forked": len([repo for repo in repos.get("values", []) if repo["parent"] !=None]),
                },
                "followers": 0,
                "languages": self._get_languages_used(repos),
                "topics": [],
            }
        except Exception as e:
            return {"error": str(e)}


    def _get_languages_used(self, repos):
        languages = set()
        for repo in repos.get("values", []):
            if "language" in repo:
                languages.add(repo["language"])
        return list(languages)

    def _make_request(self, endpoint):
        import requests
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()