```
usage: tweet.py [-h] --twitter_consumer_key TWITTER_CONSUMER_KEY --twitter_consumer_secret
                TWITTER_CONSUMER_SECRET --twitter_access_key TWITTER_ACCESS_KEY
                --twitter_access_secret TWITTER_ACCESS_SECRET --soundcloud_client_id
                SOUNDCLOUD_CLIENT_ID
                id

Tweets the latest soundcloud comment from Soundcloud User

positional arguments:
  id                    A Soundcloud user's ID

optional arguments:
  -h, --help            show this help message and exit
  --twitter_consumer_key TWITTER_CONSUMER_KEY
                        Your Twitter app's consumer key [env var: TWITTER_CONSUMER_KEY]
  --twitter_consumer_secret TWITTER_CONSUMER_SECRET
                        Your Twitter app's consumer secret [env var: TWITTER_CONSUMER_SECRET]
  --twitter_access_key TWITTER_ACCESS_KEY
                        Your Twitter app's access key [env var: TWITTER_ACCESS_KEY]
  --twitter_access_secret TWITTER_ACCESS_SECRET
                        Your Twitter app's access secret [env var: TWITTER_ACCESS_SECRET]
  --soundcloud_client_id SOUNDCLOUD_CLIENT_ID
                        A Soundcloud app's client ID [env var: SOUNDCLOUD_CLIENT_ID]

 If an arg is specified in more than one place, then commandline values override environment
variables which override defaults.
```
