import configargparse
import sys
import os
import tweepy
import urllib.request, json

parser = configargparse.ArgParser(description="Tweets the latest soundcloud comment from Soundcloud User")
parser.add('--twitter_consumer_key', help="Your Twitter app's consumer key", env_var='TWITTER_CONSUMER_KEY', required=True)
parser.add('--twitter_consumer_secret', help="Your Twitter app's consumer secret", env_var='TWITTER_CONSUMER_SECRET', required=True)
parser.add('--twitter_access_key', help="Your Twitter app's access key", env_var='TWITTER_ACCESS_KEY', required=True)
parser.add('--twitter_access_secret', help="Your Twitter app's access secret", env_var='TWITTER_ACCESS_SECRET', required=True)
parser.add('--soundcloud_client_id', help="A Soundcloud app's client ID", env_var='SOUNDCLOUD_CLIENT_ID', required=True)
parser.add('soundcloud_user_id', metavar='id', type=int, help="A Soundcloud user's ID")

args = parser.parse_args()

auth = tweepy.OAuthHandler(args.twitter_consumer_key, args.twitter_consumer_secret)
auth.set_access_token(args.twitter_access_key, args.twitter_access_secret)

api = tweepy.API(auth)

def get_last_tweet_body():
  tweets = api.user_timeline(id = api.me().id, count = 1)
  if len(tweets) == 0:
      return
  return tweets[0].text.split('\n')[0]

last_body = get_last_tweet_body()
soundcloud_api_url = f"https://api-v2.soundcloud.com/users/{args.soundcloud_user_id}/comments?client_id={args.soundcloud_client_id}"
with urllib.request.urlopen(soundcloud_api_url) as url:
  data = json.loads(url.read().decode())
  latest_comment = data['collection'][0]
  body = latest_comment["body"]
  permalink = latest_comment["track"]["permalink_url"]
  output = f"{body}\n{permalink}"
  if body != last_body:
    api.update_status(output)
    print(f"Tweeted: {body}")
  else:
    print('nothing tweeted')
