import os
from datetime import datetime

from twitter import *
from twitter.stream import TwitterStream

import keys


track_word = 'にゃーん'
except_word = 'がにゃーんしました'

TOKEN_FILE = os.path.expanduser('./.token')
if not os.path.exists(TOKEN_FILE):
    oauth_dance(keys.APP_NAME, keys.CONSUMER_KEY, keys.CONSUMER_SECRET, TOKEN_FILE)

token, token_secret = read_token_file(TOKEN_FILE)

auth=OAuth(token, token_secret, keys.CONSUMER_KEY, keys.CONSUMER_SECRET)
t = Twitter(auth=auth)

twitter_userstream = TwitterStream(auth=auth, domain='userstream.twitter.com')
tweet_itr = twitter_userstream.user()

for tweet in tweet_itr:
	if tweet.get('text'):
		if track_word in tweet['text'] and not except_word in tweet['text']:
			timestamp = datetime.fromtimestamp(int(tweet['timestamp_ms'])/1000)
			tweet_text = str(timestamp)+'\n'+tweet['user']['name']+ except_word
			print(tweet_text)
			if not tweet['user']['protected']:
				try:
					t.statuses.update(status=tweet_text)
				except:
					pass
