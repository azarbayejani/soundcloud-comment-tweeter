import sys
import os
import tweepy
import urllib.request, json

CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

# You can grab this by looking at Soundcloud API requests in the Network tab of your browser
SOUNDCLOUD_CLIENT_ID=os.environ['SOUNDCLOUD_CLIENT_ID']

if len(sys.argv) < 2:
  exit('usage: python tweet.py <soundcloud_user_id>')
user_id = sys.argv[1]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

def get_last_tweet_body():
  tweets = api.user_timeline(id = api.me().id, count = 1)
  if len(tweets) == 0:
      return
  return tweets[0].text.split('\n')[0]

last_body = get_last_tweet_body()
soundcloud_api_url = f"https://api-v2.soundcloud.com/users/{user_id}/comments?client_id={SOUNDCLOUD_CLIENT_ID}"
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
