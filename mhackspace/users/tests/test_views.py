from django.test import RequestFactory
from django.http import Http404

from test_plus.test import TestCase

from ..views import (
    UserRedirectView,
    UserDetailView,
    UserUpdateView
)


class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.userTwo = self.make_user(username='username2')
        self.factory = RequestFactory()


class TestUserDetailView(BaseUserTestCase):
    def setUp(self):
        super(TestUserDetailView, self).setUp()
        self.client.login(
            username=self.user.username,
            password=self.user.password)  # defined in fixture or with factory in setUp()

    def test_view_not_logged_in_404s(self):
        self.client.logout()
        response = self.client.get('/users/', {'username': self.user.username}, follow=True)
        self.assertEqual(
            response.status_code,
            404
        )

    def test_user_profile_does_not_exist_404s(self):
        response = self.client.get('/users/', {'username': 'does-not-exist'}, follow=True)
        self.assertEqual(
            response.status_code,
            404
        )

    def test_view_anothers_profile_404s(self):
        response = self.client.get(
            '/users/',
            {'username': self.userTwo.username},
            follow=True)
        self.assertEqual(
            response.status_code,
            404
        )

    def test_view_users_own_profile_succeeds(self):
        response = self.client.get('/users/%s' % self.user.username, follow=True)
        self.assertEqual(
            response.status_code,
            200
        )


class TestUserRedirectView(BaseUserTestCase):

    def test_get_redirect_url(self):
        # Instantiate the view directly. Never do this outside a test!
        view = UserRedirectView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        view.request = request
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            view.get_redirect_url(),
            '/users/testuser/'
        )


class TestUserUpdateView(BaseUserTestCase):

    def setUp(self):
        # call BaseUserTestCase.setUp()
        super(TestUserUpdateView, self).setUp()
        # Instantiate the view directly. Never do this outside a test!
        self.view = UserUpdateView()
        # Generate a fake request
        request = self.factory.get('/fake-url')
        # Attach the user to the request
        request.user = self.user
        # Attach the request to the view
        self.view.request = request

    def test_get_success_url(self):
        # Expect: '/users/testuser/', as that is the default username for
        #   self.make_user()
        self.assertEqual(
            self.view.get_success_url(),
            '/users/testuser/'
        )

    def test_get_object(self):
        # Expect: self.user, as that is the request's user object
        self.assertEqual(
            self.view.get_object(),
            self.user
        )
