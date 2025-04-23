# Git Profile API

## Overview
The Git Profile API is a Flask-based application that aggregates data from GitHub and Bitbucket to provide a unified profile for organizations and teams. This API allows users to retrieve information about public repositories, followers, languages used, and topics associated with the specified GitHub organization and Bitbucket team.

## Features
- Merges profiles from GitHub and Bitbucket into a single response.
- Provides total counts of public repositories, separated by original and forked.
- Returns total watcher/follower counts.
- Lists and counts languages used across all public repositories.
- Lists and counts repository topics.

## Project Structure
```
git-profile-api
├── src
│   ├── app.py                     # Entry point of the application
│   ├── services
│   │   ├── github_service.py       # Service for interacting with GitHub API
│   │   └── bitbucket_service.py    # Service for interacting with Bitbucket API
│   ├── controllers
│   │   └── profile_controller.py    # Controller for handling profile requests
│   ├── models
│   │   └── profile_model.py        # Model for structuring profile data
│   ├── utils
│   │   └── api_client.py           # Utility functions for API requests
│   └── tests
│       ├── test_app.py             # Unit tests for the application
├── requirements.txt                 # Project dependencies
├── README.md                        # Project documentation
└── .gitignore                       # Files to ignore in version control
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/sarada01/git-profile-api.git
   cd git-profile-api
   ```
2. Install the required dependencies:
   Enable the vitural environment for python to avoid any version conflicts
   NOTE:  This code has been validated on Python 3.6.8 AND 3.9
   ```
   python -m venv .venv
   ```
   Activate virtual environment in windows environment:
   
   ```
   .venv\scripts\activate
   ```
   Activate virtual environment in MAC environment:
   ```
   source .venv/bin/activate
   ```
   Install Dependencies required for running this application
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Start the Flask application:

   ```
   python src/app.py
   ```

2. Access the API endpoint to merge profiles: <BR>
   **NOTE:** The application default would start at 5000 port.  Please make sure no other app is running at PORT = 5000 <BR >
   URL: http://127.0.0.1:5000 should provide the default welcome message("Welcome to the Profile API!") to confirm the server has started successfuly.
   ```
   GET: http://127.0.0.1:5000/api/profile?github_org=<GITHUB_ORG>&bitbucket_team=<BITBUCKET_TEAM>
   ```

   Replace `<GITHUB_ORG>` with the desired GitHub organization name and `<BITBUCKET_TEAM>` with the desired Bitbucket team name.

## API Response
The API will return a JSON response containing the merged profile data, including:
- Total number of public repositories (original and forked)
- Total watcher/follower count
- List and count of languages used
- List and count of repository topics

## Testing
**NOTE:** 
- Before launching the test case, please cancel/disconnect the previous instance of the application 
- Please ensure that, your Virtual environment is still active.  <BR>

To run the unit tests, use the following command:
```
pytest src/tests
```
