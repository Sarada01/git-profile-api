from flask import Flask, request, jsonify
from controllers.profile_controller import merge_profile

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to the Profile API!"

@app.route('/api/profile', methods=['POST'])
def get_profile():
    return merge_profile()

if __name__ == '__main__':
    app.run(debug=False)