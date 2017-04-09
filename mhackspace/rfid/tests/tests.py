import sys
import requests

from io import StringIO
from django.core.management import call_command
from test_plus.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient

from mhackspace.rfid.models import Device
from mhackspace.user.models import User


# http://www.django-rest-framework.org/api-guide/testing/

class MigrationTestCase(TestCase):

    def testRollback(self):
        out = StringIO()
        sys.stout = out
        call_command('migrate', 'rfid', 'zero', stdout=out)
        call_command('migrate', 'rfid', stdout=out)
        self.assertIn("... OK\n", out.getvalue())

class ApiTests(TestCase):
    def setUp(self):
        Device(name='device01').save()
        User(name='User01').save()
        Rfid(code=1, user=1).save()

    def testAuth(self):
        factory = APIRequestFactory()
        request = factory.get('/rfid/')

    def testSamsMadness(self):
        client = RequestsClient()
        response = client.post(
            'http://127.0.0.1:8180/api/v1/rfidAuth/?format=json',
            data={'rfid':'1', 'device': '1'})
        print(response)
        assert response.status_code == 200
        self.assertEquals(response.json().get('results'), [{'name': 'device01'}])


    def testAuthUserWithDevice(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8180/api/v1/rfid/?format=json')
        assert response.status_code == 200
        self.assertEquals(response.json().get('results'), [{'name': 'device01'}])


    def testFetchDeviceList(self):
        client = RequestsClient()
        response = client.get('http://127.0.0.1:8180/api/v1/rfid/?format=json')
        assert response.status_code == 200
        self.assertEquals(response.json().get('results'), [{'name': 'device01'}])


