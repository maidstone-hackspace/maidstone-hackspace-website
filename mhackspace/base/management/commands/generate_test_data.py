import uuid
import random
from django.contrib.auth.hashers import make_password
from autofixture import AutoFixture
from autofixture.generators import (
    ImageGenerator,
    IntegerGenerator,
    ChoicesGenerator,
    Generator,
    LoremWordGenerator)
from django.core.management.base import BaseCommand
from django.core.management import call_command
from mhackspace.base.models import BannerImage
from mhackspace.feeds.models import Article, Feed
from mhackspace.users.models import User, Rfid
from mhackspace.blog.models import Category, Post
from mhackspace.rfid.models import Device, DeviceAuth


class ImageFixture(AutoFixture):
    class Values:
        scaled_image = ImageGenerator(width=800, height=300, sizes=((1280, 300),))


def RfidFixture():
    while True:
        yield str(uuid.uuid4())[0:4]


class RfidGenerator(Generator):
    def generate(self):
        return str(uuid.uuid4())[0:4]


class Command(BaseCommand):
    help = 'Build test data for development environment'

    def handle(self, *args, **options):
        feeds = AutoFixture(Article, generate_fk=True)
        feeds.create(10)

        feed = AutoFixture(Feed)
        feed.create(10)

        post = AutoFixture(Post)
        post.create(10)

        categorys = AutoFixture(Category)
        categorys.create(10)

        # load known data
        call_command('loaddata', 'mhackspace/users/fixtures/groups.json', verbose=0)


        User.objects.all().delete()
        users = AutoFixture(User, field_values={
            'title': ChoicesGenerator(values=('Mr', 'Mrs', 'Emperor', 'Captain')),
            'password': make_password('autofixtures'),
            'active': True,
            'username': ChoicesGenerator(values=('Bob', 'Jane', 'Adam', 'Alice', 'Bill', 'Jill', 'Sam', 'Oly'))
        }, generate_fk=True)
        users.create(8)
        users = AutoFixture(User, field_values={
            'title': 'Mr',
            'username': 'admin',
            'password': make_password('autofixtures'),
            'is_superuser': True,
            'is_staff': True,
            'is_active': True
        }, generate_fk=True)
        users.create(1)

        Rfid.objects.all().delete()
        Device.objects.all().delete()
        DeviceAuth.objects.all().delete()

        rfid = AutoFixture(
            Rfid,
            field_values={
                'code': RfidGenerator(),
                'description': LoremWordGenerator()})
        rfid.create(20)

        device = AutoFixture(Device, field_values={
            'name': ChoicesGenerator(values=('Door', 'Printer', 'Laser Cutter', ''))
        })
        device.create(5)

        deviceauth = AutoFixture(DeviceAuth)
        deviceauth.create(5)

        feed = AutoFixture(Feed)
        feed.create(10)

        feeds = AutoFixture(Article)
        feeds.create(10)

        banners = ImageFixture(BannerImage)
        banners.create(10)
        self.stdout.write(
            self.style.SUCCESS(
                'Finished creating test data'))

