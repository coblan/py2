import requests
from urlparse import parse_qs
from requests_oauthlib import OAuth1

consumer_key='rkGfOADVkeOUxiylvU5CpBVU1'
consumer_secret='Tttwjj4X2JNCk6sPOQIPjyndMczObFbyQC6OsgcfwLhz2Eug21'
access_token='1723436838-MtoW8OCeARhPDNmKcqQfRBZYNsNqNFY1wrHaIUz'
access_token_secret='3jMLmhzyuSL9wt2YvT19LMGdtM4Oyi5GtHqt8r1qIL9JA'

class Twit(object):
    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token,
                 access_token_secret,):
        self.consumer_key=consumer_key
        self.consumer_secret=consumer_secret
        self.access_token=access_token
        self.access_token_secret=access_token_secret
    
    def run(self):
        self.request_response()
        self.redirect_user()
        self.oauth_token()
        self.access_setting()
        
    def request_response(self):
        url = 'https://api.twitter.com/oauth/request_token'
        auth = OAuth1(self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret)
        r = requests.post(url, auth=auth)
        credentials = parse_qs(r.content)
        self.resource_owner_key = credentials.get('oauth_token')[0]
        self.resource_owner_secret = credentials.get('oauth_token_secret')[0]        
    
    def redirect_user(self):
        base_authorization_url = 'https://api.twitter.com/oauth/authorize'
        base_authorization_url +='?oauth_token=%s'%self.resource_owner_key
        print('Please go here and authorize,',base_authorization_url)
        self.verifier = raw_input('Please input the verifier')  
    
    def oauth_token(self):
        access_token_url = 'https://api.twitter.com/oauth/access_token'
        oauth = OAuth1(client_key=self.consumer_key,
                           client_secret=self.consumer_secret,
                           resource_owner_key=self.resource_owner_key,
                           resource_owner_secret=self.resource_owner_secret,
                           verifier=self.verifier)
        r = requests.post(url=access_token_url, auth=oauth)
        print(r.content)
        credentials = parse_qs(r.content)
        self.resource_owner_key = credentials.get('oauth_token')[0]
        self.resource_owner_secret = credentials.get('oauth_token_secret')[0]   
    
    def access_setting(self):
        protected_url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
        oauth = OAuth1(client_key=self.consumer_key,
                        client_secret=self.consumer_secret,
                        resource_owner_key=self.resource_owner_key,
                        resource_owner_secret=self.resource_owner_secret)
        r = requests.get(url=protected_url, auth=oauth)
        print(r.text)


if __name__ =='__main__':
    t=Twit(consumer_key, consumer_secret, access_token, access_token_secret)
    t.run()