from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from mhackspace.rfid.models import Device,  Rfid
from mhackspace.rfid.serializers import DeviceSerializer, AuthSerializer
from django.shortcuts import get_list_or_404, get_object_or_404


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# https://medium.com/django-rest-framework/django-rest-framework-viewset-when-you-don-t-have-a-model-335a0490ba6f
class AuthUserWithDeviceViewSet(viewsets.ViewSet):
    http_method_names = ['post']
    serializer_class = AuthSerializer

    def list(self, request):
        serializer = AuthSerializer(
            instance={'name': '1', 'rfid': '1', 'device_id': '1'})
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            rfid = Rfid.objects.get(code=request.data.get('rfid'))
            device = Device.objects.get(user=rfid.user, identifier=request.data.get('device_id'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AuthSerializer(
            instance={'name': device.name, 'rfid': rfid.code, 'device_id': device.identifier})
        return Response(serializer.data, status=200)
