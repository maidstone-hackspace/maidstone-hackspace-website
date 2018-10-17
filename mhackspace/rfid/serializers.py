from rest_framework import serializers
from mhackspace.rfid.models import Device


class Task(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'owner', 'status'):
            setattr(self, field, kwargs.get(field, None))


class DeviceSerializer(serializers.ModelSerializer):
    added_date = serializers.DateTimeField(format='iso-8601')

    class Meta:
        model = Device
        fields = ('__all__')


class AuthSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    rfid = serializers.CharField(max_length=255)
    device = serializers.CharField(max_length=255)

