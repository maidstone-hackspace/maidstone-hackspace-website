from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class SassStorageFix(S3Boto3Storage):
    base_url = settings.AWS_S3_ENDPOINT_URL


class MediaStorage(S3Boto3Storage):
    base_url = settings.AWS_S3_ENDPOINT_URL
    location = settings.MEDIAFILE_LOCATION


class StaticStorage(S3Boto3Storage):
    base_url = settings.AWS_S3_ENDPOINT_URL
    location = settings.STATICFILE_LOCATION
