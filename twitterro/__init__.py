from httplib2 import Http
from twitterro.base import EndPoint
from twitterro.oauthclient import OAuthHttp
from twitterro.remote_objects import *
import sys

class User(EndPoint):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.is_plural = True

    def show(self, **kwargs):
        # TODO: handle this gracefully if the values aren't provided
        if "id" in kwargs:
            extra = "id=%s" % kwargs['id']
        else:
            extra = "screen_name=%s" % kwargs['screen_name']
        return self.do_get('show.json?%s' % extra)

class Followers(EndPoint):
    def ids(self, id = None, screen_name = None, user_id = None, cursor = -1):
        if id:
            return self.do_get('/ids/%s.json?', id)
        else:
            return self.do_get('ids.json?%s&cursor=%d' % (
                screen_name and "screen_name=" + screen_name or "user_id=" + user_id,
                cursor
            ))

class Friendships(EndPoint):
    def create(self, id = None, user_id = None, screen_name = None, follow = 'false'):
        if id:
            full_url = 'create/%s.json?' % id
        else:
            full_url = 'create.json?user_id=%s&screen_name=%s' % (user_id, screen_name)
        return self.do_post_with_remote_object(full_url + ('&follow=%s' % follow),
            remote_object=UserRemoteObject)

    def destroy(self, id =  None, user_id = None, screen_name = None):
        if id:
            full_url = 'destroy/%s.json?' % id
        else:
            full_url = 'destroy.json?user_id=%s&screen_name=%s' % (user_id, screen_name)
        return self.do_post_with_remote_object(full_url, remote_object=UserRemoteObject)

    def exists(self, user_a, user_b):
        return self.do_boolean_get('exists.json?user_a=%s&user_b=%s' % (user_a, user_b))

    def show(self, source_id = None, source_screen_name = None, target_id = None, target_screen_name = None):
        if not source_id and not source_screen_name:
            raise Exception("source_id or source_screen_name is required")
        if not target_id and not target_screen_name:
            raise Exception("target_id or target_screen_name is required")

        url = "show.json?"
        url += source_id and "source_id=%s" % source_id or "source_screen_name=%s" % source_screen_name
        url += target_id and "&target_id=%s" % target_id or "&target_screen_name=%s" % target_screen_name
        return self.do_get(url)

def add_twitter_properties(twitter):
    twitter.users = User(http = twitter)
    twitter.followers = Followers(http = twitter)
    twitter.friendships = Friendships(http = twitter)

class Twitter(Http):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.api_url = 'https://twitter.com'
        add_twitter_properties(self)

class OAuthTwitter(OAuthHttp):
    request_token_url = 'https://twitter.com/oauth/request_token'
    access_token_url = 'https://twitter.com/oauth/access_token'
    authorization_url = 'http://twitter.com/oauth/authorize'
    signin_url = 'http://twitter.com/oauth/authenticate'

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        # callback_url isn't necessary for Twitter
        self.callback_url = 'callback_url' in kwargs and kwargs['callback_url'] or ''
        self.api_url = 'https://twitter.com'
        add_twitter_properties(self)



