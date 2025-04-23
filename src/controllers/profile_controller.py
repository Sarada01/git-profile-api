import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from flask import Blueprint, request, jsonify
from services.github_service import GitHubService
from services.bitbucket_service import BitbucketService
from models.profile_model import Profile

profile_blueprint = Blueprint('profile', __name__)

github_service = GitHubService(org_name='example_org')
bitbucket_service = BitbucketService(team_name='example_team')

@profile_blueprint.route('/merge_profile', methods=['POST'])
def merge_profile():
    data = request.json
    bitbucket_team = data.get('bitbucket_team')
    github_org = data.get('github_org')
    

    if not github_org or not bitbucket_team:
        return jsonify({'error': 'Both github_org and bitbucket_team are required'}), 400

    # Update the org_name for GitHubService dynamically
    bitbucket_service.team_name = bitbucket_team
    github_service.org_name = github_org
    

    # Call get_organization_data without arguments
    bitbucket_data = bitbucket_service.get_team_data()
    github_data = github_service.get_organization_data()
    

    if github_data is None or bitbucket_data is None:
        return jsonify({'error': 'Failed to fetch data from GitHub or Bitbucket'}), 500

    merged_profile = Profile.merge(github_data, bitbucket_data)

    return jsonify(merged_profile), 200