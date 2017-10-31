import logging
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from django.views.generic import ListView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from mhackspace.users.models import Rfid
from mhackspace.rfid.models import Device, DeviceAuth
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
            Device.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        try:
            rfid = Rfid.objects.get(code=request.data.get('rfid'))
            device = Device.objects.get(identifier=request.data.get('device'))
            deviceAuth = DeviceAuth.objects.get(device=device.identifier, rfid=rfid.id)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
        # except:
        #     logger.exception("An error occurred")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = AuthSerializer(
            instance={'name': device.name, 'rfid': rfid.code, 'device': device.identifier})
        return Response(serializer.data, status=200)


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
