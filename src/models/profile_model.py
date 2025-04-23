class Profile:
    def __init__(self, org_name, team_name):
        self.org_name = org_name
        self.team_name = team_name
        self.public_repos = {
            'total': 0,
            'original': 0,
            'forked': 0
        }
        self.followers_count = 0
        self.languages = set()
        self.topics = set()

    def add_repo(self, is_fork, language):
        self.public_repos['total'] += 1
        if is_fork:
            self.public_repos['forked'] += 1
        else:
            self.public_repos['original'] += 1
        
        if language:
            self.languages.add(language)

    def add_follower(self, count):
        self.followers_count += count

    def add_topic(self, topic):
        if topic:
            self.topics.add(topic)

    def get_profile_summary(self):
        return {
            'organization': self.org_name,
            'team': self.team_name,
            'public_repos': self.public_repos,
            'followers_count': self.followers_count,
            'languages': list(self.languages),
            'topics': list(self.topics)
        }

    @staticmethod
    def merge(github_data, bitbucket_data):
        profile = Profile(
            org_name=github_data.get('organization', 'Unknown'),
            team_name=bitbucket_data.get('team', 'Unknown')
        )
        # Merge public repos
        profile.public_repos['total'] = (
            github_data.get('public_repos', {}).get('total', 0) +
            bitbucket_data.get('public_repos', {}).get('total', 0)
        )
        profile.public_repos['original'] = github_data.get('public_repos', {}).get('original', 0)
        profile.public_repos['forked'] = github_data.get('public_repos', {}).get('forked', 0)

        # Merge followers
        profile.add_follower(github_data.get('watchers_count', 0))
        profile.add_follower(bitbucket_data.get('followers', 0))

        # Merge languages
        profile.languages.update(github_data.get('languages', []))
        profile.languages.update(bitbucket_data.get('languages', []))

        # Merge topics
        profile.topics.update(github_data.get('topics', []))
        profile.topics.update(bitbucket_data.get('topics', []))

        return profile.get_profile_summary()