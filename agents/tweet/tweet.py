import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

# Enter API tokens below
consumer_key = os.getenv('TWITTER_API_KEY')
consumer_secret = os.getenv('TWITTER_API_SECRET_KEY')
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# V1 Twitter API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

def print_text_tweet(text):
    client.create_tweet(text=text)
    print("Tweeted with text!")

def print_image_tweet(text, image_path, multiple=False):
    """If you want to tweet an image, pass the path of the image as a string or a list of strings for multiple images."""
    if multiple:
        media_ids = []
        for image in image_path:
            media_id = api.media_upload(filename=image).media_id_string
            media_ids.append(int(media_id))
        print(media_ids)
        client.create_tweet(text=text, media_ids=media_ids)
    else:
        media_id = api.media_upload(filename=image_path).media_id_string
        client.create_tweet(text=text, media_ids=[media_id])
    print("Tweeted with image!")


# Example usage
# print_text_tweet("Hello, world! This is a test tweet from Tweepy.")
# print_image_tweet("Hello, world! This is a test tweet with an image from Tweepy.", ["image.png", "tweet.jpg"])
