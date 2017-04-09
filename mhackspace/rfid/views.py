from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from mhackspace.rfid.models import Device,  Rfid
from mhackspace.rfid.serializers import DeviceSerializer, AuthSerializer
from django.shortcuts import get_list_or_404, get_object_or_404


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


#https://medium.com/django-rest-framework/django-rest-framework-viewset-when-you-don-t-have-a-model-335a0490ba6f
class AuthUserWithDeviceViewSet(viewsets.ViewSet):
    # http_method_names = ['get', 'post', 'head']
    serializer_class = AuthSerializer

    def list(self, request):
        serializer = AuthSerializer(instance={'name': '1','rfid': '1', 'device_id': '1'})
        return Response(serializer.data)

    def post(self, request, format=None):
        rfid = Rfid.objects.get(code=request.GET.get('rfid_id'))

        print(rfid.user.device__set(device=request.GET.get('rfid_id')))
         # = get_object_or_404(Disease, pk=disease_id)


        # Device(rfid, device)
        serializer = AuthSerializer(instance={'name': '1', 'rfid': '1', 'device_id': '1'})
        return Response(serializer.data)
