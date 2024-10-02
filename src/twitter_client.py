from tweety import Twitter
from src.config import AUTH_TOKEN

class TwitterClient:
    def __init__(self):
        self.app = Twitter("session")
        self.app.load_auth_token(AUTH_TOKEN)

    def get_tweets(self, username):
        return list(self.app.get_tweets(username))

    def get_tweet_detail(self, tweet_id):
        return self.app.tweet_detail(tweet_id)
