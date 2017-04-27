import logging
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from mhackspace.rfid.models import Device,  Rfid, DeviceAuth
from mhackspace.rfid.serializers import DeviceSerializer, AuthSerializer
from django.core.exceptions import ObjectDoesNotExist, ValidationError

logger = logging.getLogger(__name__)


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# https://medium.com/django-rest-framework/django-rest-framework-viewset-when-you-don-t-have-a-model-335a0490ba6f
class AuthUserWithDeviceViewSet(viewsets.ViewSet):
    # http_method_names = ['post']
    serializer_class = AuthSerializer

    def list(self, request):
        serializer = DeviceSerializer(
            DeviceAuth.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            rfid = Rfid.objects.get(code=request.data.get('rfid'))
            device = Device.objects.get(identifier=request.data.get('device'))
            deviceAuth = DeviceAuth.objects.get(device=device.identifier, rfid=rfid.id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError:
        # except:
        #     logger.exception("An error occurred")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = AuthSerializer(
            instance={'name': device.name, 'rfid': rfid.code, 'device': device.identifier})
        return Response(serializer.data, status=200)
