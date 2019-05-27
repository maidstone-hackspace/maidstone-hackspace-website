import logging
import jwt
from jwt import ExpiredSignatureError
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from django.views.generic import ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from mhackspace.base.tasks import matrix_message
from mhackspace.users.models import Rfid
from mhackspace.rfid.models import Device, AccessLog
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
        serializer = DeviceSerializer(
            Device.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            data = jwt.decode(request.data["data"], settings.RFID_SECRET, algorithms=['HS256'])
        except ExpiredSignatureError:
            data = jwt.decode(request.data["data"], settings.RFID_SECRET, algorithms=['HS256'], verify=False)
            logger.warning(f"Signature expired for {data.get('rfid_code')} on device {data.get('device_id')}")
            return Response(jwt.encode({"authenticated": False}, settings.RFID_SECRET), status=status.HTTP_403_FORBIDDEN)
        except jwt.exceptions.InvalidTokenError as e:
            logger.warning(f'Invalid JWT {e} : {request.data["data"]}')
            return Response(jwt.encode({"authenticated": False}, settings.RFID_SECRET),
                            status=status.HTTP_403_FORBIDDEN)

        if data.get("rfid_code") is None or data.get("rfid_code") is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            rfid = Rfid.objects.get(code=data["rfid_code"])
        except Rfid.DoesNotExist:
            logger.warning(f"Unable to find valid rfid {data['rfid_code']}")
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            device = Device.objects.get(identifier=data["device_id"])
        except Device.DoesNotExist:
            logger.warning(f"Unable to find valid device {data['device_id']}")
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            member = device.users.get(pk=rfid.user_id)
            matrix_message(
                f"{member.username} has just entered {device.name}"
            )
            AccessLog.objects.create(rfid=rfid, device=device, success=True)
            return Response(jwt.encode({"authenticated": True, "username": member.username}, settings.RFID_SECRET))
        except ObjectDoesNotExist:
            AccessLog.objects.create(rfid=rfid, device=device, success=False)
            return Response(jwt.encode({"authenticated": False}, settings.RFID_SECRET), status=status.HTTP_403_FORBIDDEN)


class RfidCardsListView(LoginRequiredMixin, ListView):
    template_name = 'users/rfid_form.html'
    context_object_name = 'rfids'
    paginate_by = 50
    model = Rfid

    def get_queryset(self):
        return Rfid.objects.filter(user=self.request.user)


class RfidCardsUpdateView(LoginRequiredMixin, CreateView):
    fields = ['code', 'description', ]
    model = Rfid
    success_url = '/users/access-cards'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(RfidCardsUpdateView, self).form_valid(form)


class RfidCardsDeleteView(LoginRequiredMixin, DeleteView):
    model = Rfid
    success_url = '/users/access-cards'
