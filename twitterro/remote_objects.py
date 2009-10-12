from httplib2 import Http
from remoteobjects import RemoteObject, fields, ListObject

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

class FollowersRemoteObject(RemoteObject):
    ids = fields.Field()
    next_cursor = fields.Field()
    previous_cursor = fields.Field()

class FriendshipsRemoteObject(RemoteObject):
    relationship = fields.Field()


