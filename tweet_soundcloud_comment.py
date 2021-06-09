import configargparse
import html
import asyncio
import sys
import os
import tweepy
from pyppeteer import launch

parser = configargparse.ArgParser(description="Tweets the latest Soundcloud comment from Soundcloud user ID")
parser.add('--twitter_consumer_key', help="Your Twitter app's consumer key", env_var='TWITTER_CONSUMER_KEY', required=True)
parser.add('--twitter_consumer_secret', help="Your Twitter app's consumer secret", env_var='TWITTER_CONSUMER_SECRET', required=True)
parser.add('--twitter_access_key', help="Your Twitter app's access key", env_var='TWITTER_ACCESS_KEY', required=True)
parser.add('--twitter_access_secret', help="Your Twitter app's access secret", env_var='TWITTER_ACCESS_SECRET', required=True)
parser.add('soundcloud_username', metavar='username', type=str, help="A Soundcloud username")

def get_last_tweet():
  tweets = api.user_timeline(id = api.me().id, count = 1, include_entities = True, tweet_mode='extended')
  if len(tweets) == 0:
      return None, None
  if len(tweets[0].entities['urls']) != 1:
      return None, None
  return tweets[0].full_text.split('\n')[0], tweets[0].entities['urls'][0]['expanded_url']

args = parser.parse_args()

auth = tweepy.OAuthHandler(args.twitter_consumer_key, args.twitter_consumer_secret)
auth.set_access_token(args.twitter_access_key, args.twitter_access_secret)

api = tweepy.API(auth)

last_body, last_url  = get_last_tweet()

soundcloud_url = f"http://soundcloud.com/{args.soundcloud_username}/comments"

print(last_body)
print(last_url)

async def main():
  browser = await launch({ 'headless': True })
  page = await browser.newPage()
  await page.goto(soundcloud_url)
  await page.waitForSelector('.commentBadge')

  link = await page.querySelector('.commentBadge__title a')
  permalink = await page.evaluate('(link) => link.href', link)
  body_container = await page.querySelector('.commentBadge__body')
  body = await page.evaluate('(body_container) => body_container.innerText', body_container)

  output = f"{body}\n{permalink}"
  if html.escape(body) != last_body or permalink != last_url:
    api.update_status(output)
    print(f"Tweeted: {body}")
  else:
    print('nothing tweeted')

asyncio.get_event_loop().run_until_complete(main())
