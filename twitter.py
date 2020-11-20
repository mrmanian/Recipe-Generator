# Import required packages
import os
from tweepy import OAuthHandler, Cursor, API
from dotenv import load_dotenv
import pytz

# Load the .env file
load_dotenv()

# Setup access to Twitter API using keys stored in .env file
auth = OAuthHandler(os.getenv("CONSUMER_API_KEY"), os.getenv("CONSUMER_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_SECRET"))
api = API(auth, wait_on_rate_limit=True)


class Twitter:
    def __init__(self, food):
        self.food = food

    # Get list of tweets related to the food
    def tweets(self):
        food = self.food

        # Create Cursor object and search for tweets
        status = Cursor(api.search, q=food, tweet_mode="extended", lang="en").items(7)

        # Gather tweets and relevant information from status and store into a list
        tweets = [
            [
                '"' + tweet.full_text + '"',
                " -@" + tweet.user.screen_name,
                tweet.created_at.astimezone(pytz.timezone("US/Eastern")).strftime(
                    "%I:%M %p · %b %d, %Y"
                ),
                "https://twitter.com/"
                + tweet.user.screen_name
                + "/status/"
                + str(tweet.id),
            ]
            for tweet in status
        ]

        return tweets
