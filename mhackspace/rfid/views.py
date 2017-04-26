import logging
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from mhackspace.rfid.models import Device,  Rfid
from mhackspace.rfid.serializers import DeviceSerializer, AuthSerializer
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# https://medium.com/django-rest-framework/django-rest-framework-viewset-when-you-don-t-have-a-model-335a0490ba6f
class AuthUserWithDeviceViewSet(viewsets.ViewSet):
    # http_method_names = ['post']
    serializer_class = AuthSerializer

    def list(self, request):
        serializer = AuthSerializer(
            instance={'name': '1', 'rfid': '1', 'device': '1'})
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            rfid = Rfid.objects.get(code=request.data.get('rfid'))
            device = Device.objects.get(user=rfid.user, identifier=request.data.get('device'))
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            logger.exception("An error occurred")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = AuthSerializer(
            instance={'name': device.name, 'rfid': rfid.code, 'device': device.identifier})
        return Response(serializer.data, status=200)
