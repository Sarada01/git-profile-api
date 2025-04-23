import requests
from requests.exceptions import RequestException

def get_json_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return {"error": str(e)}

def fetch_github_data(org_name):
    url = f"https://api.github.com/orgs/{org_name}"
    return get_json_response(url)

def fetch_bitbucket_data(team_name):
    url = f"https://api.bitbucket.org/2.0/teams/{team_name}/repositories"
    return get_json_response(url)