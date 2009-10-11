import sys
 
from httplib2 import Http
 
from remoteobjects import RemoteObject, fields, ListObject

class EndPoint(object):
    def __init__(self, remote_object = None, http = None):
        self.is_plural = False
        self.my_name = self.__class__.__name__.lower()
        self.remote_object = remote_object

        if not self.remote_object:
            exec("self.remote_object = " + self.my_name.capitalize() + "RemoteObject")
        self.http = http

    def get_full_url(self, url):
        return "%s/%s/%s" % (
            self.http.api_url,
            self.is_plural and self.my_name + 's' or self.my_name,
            url
        )

    def do_get(self, url):
        return self.remote_object.get(self.get_full_url(url), http = self.http)

    def do_boolean_get(self, url):
        (_headers, body) = self.http.request(self.get_full_url(url))
        return body == 'true'

    def create_remote_object_from_response(self, url, response, content, remote_object = None):
        if not remote_object:
            remote_object = self.remote_object
        ro = remote_object.get(url, http=self.http)
        ro.update_from_response(url, response, content)
        return ro

    def do_post_with_remote_object(self, url, remote_object = None):
        full_url = self.get_full_url(url)
        response, content = self.http.request(full_url, "POST")
        return self.create_remote_object_from_response(url, response, content, remote_object)
 

class UserRemoteObject(RemoteObject):
    id = fields.Field()
    name = fields.Field()
    screen_name = fields.Field()
    location = fields.Field()
    description = fields.Field()
    profile_image_url = fields.Field()
    url = fields.Field()
    protected = fields.Field()
    followers_count = fields.Field()
    profile_background_color = fields.Field()
    profile_text_color = fields.Field()
    profile_link_color = fields.Field()
    profile_sidebar_fill_color = fields.Field()
    profile_sidebar_border_color = fields.Field()
    friends_count = fields.Field()
    created_at = fields.Field()
    favourites_count = fields.Field()
    utc_offset = fields.Field()
    time_zone = fields.Field()
    profile_background_image_url = fields.Field()
    profile_background_tile = fields.Field()
    statuses_count = fields.Field()
    notifications = fields.Field()
    following = fields.Field()
    verified = fields.Field()
    status = fields.Object('Status')

class User(EndPoint):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.is_plural = True

    def show(self, **kwargs):
        return self.do_get('/%s.json?screen_name=%s' % (
            sys._getframe().f_code.co_name,
            kwargs['screen_name']
        ))

class FollowersRemoteObject(RemoteObject):
    ids = fields.Field()
    next_cursor = fields.Field()
    previous_cursor = fields.Field()


class Followers(EndPoint):
    def ids(self, id = None, screen_name = None, user_id = None, cursor = -1):
        if id:
            return self.do_get('/ids/%s.json?', id)
        else:
            return self.do_get('ids.json?%s&cursor=%d' % (
                screen_name and "screen_name=" + screen_name or "user_id=" + user_id,
                cursor
            ))

class FriendshipsRemoteObject(RemoteObject):
    relationship = fields.Field()

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



class Twitter(Http):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.api_url = 'https://twitter.com'
        self.users = User(http = self)
        self.followers = Followers(http = self)
        self.friendships = Friendships(http = self)

