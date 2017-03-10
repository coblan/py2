import tweepy

consumer_key='rkGfOADVkeOUxiylvU5CpBVU1'
consumer_secret='Tttwjj4X2JNCk6sPOQIPjyndMczObFbyQC6OsgcfwLhz2Eug21'
access_token='1723436838-MtoW8OCeARhPDNmKcqQfRBZYNsNqNFY1wrHaIUz'
access_token_secret='3jMLmhzyuSL9wt2YvT19LMGdtM4Oyi5GtHqt8r1qIL9JA'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print tweet.text