from flask import Flask, request, jsonify
from controllers.profile_controller import merge_profile

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Profile API!"

@app.route('/api/profile', methods=['GET'])
def get_profile():
    github_org = request.args.get('github_org')
    bitbucket_team = request.args.get('bitbucket_team')
    if not github_org or not bitbucket_team:
        return jsonify({'error': 'Both github_org and bitbucket_team are required'}), 400
    return merge_profile()

if __name__ == '__main__':
    app.run(debug=False)