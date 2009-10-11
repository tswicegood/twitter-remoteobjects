import os, sys
sys.path[0:0] = os.path.join(os.path.dirname(__file__), '..')
from twitter.ro.driver import *
import twitter.ro.driver
import unittest
import mox
import random
import types

class TestOfTwitter(unittest.TestCase):
    def test_has_friendships(self):
        self.assert_(getattr(Twitter(), 'friendships', False))

    def test_has_users(self):
        self.assert_(getattr(Twitter(), 'users', False))

    def test_has_followers(self):
        self.assert_(getattr(Twitter(), 'followers', False))

class TestOfEndPoint(unittest.TestCase):
    def test_do_boolean_get_returns_true_on_true(self):
        rm = EndPoint(remote_object = True, http = Twitter())
        rm.http.request = lambda _url: ({}, "true")
        self.assert_(rm.do_boolean_get("foobar"))

    def test_do_boolean_get_returns_false_on_non_true(self):
        rm = EndPoint(remote_object = True, http = Twitter())
        rm.http.request = lambda _url: ({}, "false")
        self.assertFalse(rm.do_boolean_get("barfoo"))

    def test_get_full_url_returns_proper_url(self):
        rm = EndPoint(remote_object = True, http = Twitter())
        random_value = random.randint(1, 100)
        self.assertEqual(
            "https://twitter.com/endpoint/%s" % random_value,
            rm.get_full_url(random_value)
        )

    def test_get_full_url_uses_class_name_as_first_directory(self):
        class Foo(EndPoint):
            pass

        rm = Foo(remote_object = True, http = Twitter())
        self.assertEqual(
            'https://twitter.com/foo/foobar',
            rm.get_full_url('foobar')
        )

    def test_get_full_url_uses_api_url_from_http(self):
        random_value = random.randint(1, 100)
        t = Twitter()
        t.api_url = 'https://%d.random.api' % random_value

        rm = EndPoint(remote_object = True, http = t)
        self.assertEqual(
            t.api_url,
            rm.get_full_url('foobar')[0:len(t.api_url)]
        )

    def test_uses_provided_remote_object(self):
        random_value = random.randint(1, 100)
        rm = EndPoint(remote_object = random_value)
        self.assertEqual(random_value, rm.remote_object)

    def test_loads_remote_object_of_same_name_if_remote_object_is_not_provided(self):
        class FooRemoteObject(object):
            pass
        twitter.ro.driver.FooRemoteObject = FooRemoteObject
        class Foo(EndPoint):
            pass

        rm = Foo()
        self.assert_(rm.remote_object, FooRemoteObject)

        twitter.ro.driver.FooRemoteObject = None

    def test_http_is_equal_to_what_is_passed_in(self):
        random_value = random.randint(1, 100)
        rm = EndPoint(remote_object = True, http = random_value)
        self.assertEqual(rm.http, random_value)
        
class TestOfFriendships(unittest.TestCase):
    def test_exists_returns_true_on_friendship(self):
        t = Twitter()
        t.friendships.do_boolean_get = lambda _url: True
        self.assert_(t.friendships.exists('foo', 'bar'))

    def test_exists_returns_false_on_no_friendship(self):
        t = Twitter()
        t.friendships.do_boolean_get = lambda _url: False
        self.assertFalse(t.friendships.exists('foobar', 'barfoo'))

    def test_show_throws_exception_without_proper_source(self):
        t = Twitter()
        self.assertRaises(Exception, t.friendships.show)

    def test_show_throws_exception_without_proper_target(self):
        t = Twitter()
        self.assertRaises(Exception, t.friendships.show)

if __name__ == '__main__':
    unittest.main()

