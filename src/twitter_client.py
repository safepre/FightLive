from tweety import TwitterAsync
from src.config import AUTH_TOKEN

class TwitterClient:
    async def initialize(self):
        self.app = TwitterAsync("session")
        await self.app.load_auth_token(AUTH_TOKEN)
        return self

    def iter_tweets(self, username):
        return self.app.iter_tweets(username)

    async def tweet_detail(self, tweet_id):
        return await self.app.tweet_detail(tweet_id)

    