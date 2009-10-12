import twitterro.remote_objects

# TODO: This should live in its own package
class EndPoint(object):
    def __init__(self, remote_object = None, http = None):
        self.is_plural = False
        self.my_name = self.__class__.__name__.lower()
        self.remote_object = remote_object

        if not self.remote_object:
            # TODO: abstract away the module name
            exec("self.remote_object = twitterro.remote_objects." + self.my_name.capitalize() + "RemoteObject")
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
 


