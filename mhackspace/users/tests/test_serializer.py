from test_plus.test import TestCase
from django.db import models
from allauth.utils import serialize_instance


class TestSerializeUser(TestCase):

    def setUp(self):
        self.user = self.make_user()

    def test_serialize(self):
        """check we can serialize the user object for allauth, custom types can break it"""
        result = serialize_instance(self.user)
        self.assertTrue(
            isinstance(result, dict),
        )
