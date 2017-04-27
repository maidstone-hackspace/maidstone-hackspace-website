import sys
import requests

from io import StringIO
from django.core.management import call_command
from test_plus.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import RequestsClient

from mhackspace.rfid.models import Device, Rfid, DeviceAuth
from mhackspace.users.models import User


# http://www.django-rest-framework.org/api-guide/testing/

class MigrationTestCase(TestCase):

    def testRollback(self):
        out = StringIO()
        sys.stout = out
        call_command('migrate', 'rfid', 'zero', stdout=out)
        call_command('migrate', 'rfid', stdout=out)
        self.assertIn("... OK\n", out.getvalue())


class ApiTests(TestCase):
    maxDiff = None
    def setUp(self):
        self.user = User(name='User01')
        self.user.save()
        self.device = Device(name='device01', user=self.user)
        self.device.save()
        self.rfid = Rfid(code='1', user=self.user)
        self.rfid.save()
        self.auth = DeviceAuth(rfid=self.rfid, device=self.device)
        self.save()

    def testAuth(self):
        factory = APIRequestFactory()
        request = factory.get('/rfid/')

    def testValidAuthCase(self):
        client = RequestsClient()
        response = client.post(
            'http://127.0.0.1:8180/api/v1/rfidAuth/',
            data={'rfid': '1', 'device': self.device.identifier})
        assert response.status_code == 200
        expected_result = {'rfid': self.rfid.code, 'name': 'device01', 'device': str(self.device.identifier)}
        self.assertEquals(
            response.json(),
            expected_result
            )

    def testInValidAuthCase(self):
        client = RequestsClient()
        response = client.post(
            'http://127.0.0.1:8180/api/v1/rfidAuth/',
            data={'rfid': '99', 'device': str(self.device.identifier)})
        assert response.status_code == 404

        # response = client.post(
        #     'http://127.0.0.1:8180/api/v1/rfidAuth/',
        #     data={'rfid': '1', 'device': 'test%s' % str(self.device.identifier)[3:]})
        # assert response.status_code == 404


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

