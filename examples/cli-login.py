from twitter import *
from oauth import oauth

key = raw_input("Twitter OAuth Key: ")
secret = raw_input("Twitter OAuth Secret: ")
consumer = oauth.OAuthConsumer(key=key, secret=secret)
t = OAuthTwitter()
t.consumer = consumer

t.fetch_request_token()
print "Visit the following URL, then press enter when ready"
print "    " + t.authorize_token()
raw_input()

token = t.fetch_access_token()

t.add_credentials(consumer, token)

# at this point, t is an authorized Twitter user.

