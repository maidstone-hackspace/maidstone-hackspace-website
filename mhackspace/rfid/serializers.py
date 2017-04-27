from rest_framework import serializers

from mhackspace.rfid.models import Device, DeviceAuth


class Task(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'owner', 'status'):
            setattr(self, field, kwargs.get(field, None))


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceAuth
        fields = ('__all__')


class AuthSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    rfid = serializers.CharField(max_length=255)
    # device = serializers.UUIDField(format='hex_verbose')
    device = serializers.CharField(max_length=255)

    # def create(self, validated_data):
    #     return Task(id=None, **validated_data)

    # def update(self, instance, validated_data):
    #     for field, value in validated_data.items():
    #         setattr(instance, field, value)
    #     return instance

    # class Meta:
    #     fields = ('name', )
