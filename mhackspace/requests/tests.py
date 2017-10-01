from django.test import TestCase
from mhackspace.requests.views import RequestsList, RequestForm
from mhackspace.users.models import User

# Create your tests here.

# @pytest.mark.parametrize("version", versions)
# @pytest.mark.parametrize("test_ctx, name", contexts)
# def test_context_renders(name, test_ctx, version):

        # users = AutoFixture(User, field_values={
        #     'title': 'Mr',
        #     'username': 'admin',
        #     'password': make_password('autofixtures'),
        #     'is_superuser': True,
        #     'is_staff': True,
        #     'is_active': True
        # }, generate_fk=True)

def all_user_types():
    users = AutoFixture(User, field_values={
        'title': 'Mr',
        'username': 'admin',
        'password': make_password('autofixtures'),
    }, generate_fk=True)
    yield users.create(1)

    users = AutoFixture(User, field_values={
        'title': 'Mr',
        'username': 'admin',
        'password': make_password('autofixtures'),
        'is_staff': True,
    }, generate_fk=True)
    yield users.create(1)

    users = AutoFixture(User, field_values={
        'title': 'Mr',
        'username': 'admin',
        'password': make_password('autofixtures'),
        'is_superuser': True,
        'is_staff': True,
    }, generate_fk=True)
    yield users.create(1)

class BaseUserTestCase(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()

    def testRequestView(self):
        for user in all_user_types()
            view = RequestsList()
            request = self.factory.get('/fake-url')
            request.user = user
            view.request = request


# class TestUserUpdateView(BaseUserTestCase):

#     def setUp(self):
#         # call BaseUserTestCase.setUp()
#         super(TestUserUpdateView, self).setUp()
#         # Instantiate the view directly. Never do this outside a test!
#         self.view = UserUpdateView()
#         # Generate a fake request
#         request = self.factory.get('/fake-url')
#         # Attach the user to the request
#         request.user = self.user
#         # Attach the request to the view
#         self.view.request = request

#     def test_get_success_url(self):
#         # Expect: '/users/testuser/', as that is the default username for
#         #   self.make_user()
#         self.assertEqual(
#             self.view.get_success_url(),
#             '/users/testuser/'
#         )

#     def test_get_object(self):
#         # Expect: self.user, as that is the request's user object
#         self.assertEqual(
#             self.view.get_object(),
#             self.user
#         )
