from django.db import models
from django.utils import timezone
from django.urls import reverse

from mhackspace.users.models import User
from stdimage.models import StdImageField
from stdimage.utils import UploadToAutoSlugClassNameDir
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog-category', kwargs={'category': self.slug})


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User)
    image = StdImageField(
        upload_to=UploadToAutoSlugClassNameDir(populate_from='title'),
        blank=True,
        null=True,
        variations={
            'home': {
                "width": 530,
                "height": 220,
                "crop": True}})

    description = RichTextUploadingField()
    published_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    members_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-item', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('updated_date',)

