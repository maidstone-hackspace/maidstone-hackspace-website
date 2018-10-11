from django.db import models
from django.conf import settings

from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.contrib.sites.models import Site


from martor.models import MartorField
from stdimage.validators import MinSizeValidator
from stdimage.models import StdImageField
from dynamic_filenames import FilePattern
from django.core.mail import EmailMessage
from mhackspace.base.tasks import matrix_message, twitter_message


from mhackspace.users.models import User

upload_to_pattern = FilePattern(
    filename_pattern="{model_name}/{instance.title:slug}{ext}"
)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog-category", kwargs={"category": self.slug})


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = StdImageField(
        upload_to=upload_to_pattern,
        blank=True,
        null=True,
        variations={
            "home": {"width": 530, "height": 220, "crop": True},
            "mobilethumb": {"width": 580, "height": 150, "crop": True},
            "thumbnail": {"width": 250, "height": 150, "crop": True},
            "full": {"width": 825, "height": 450, "crop": True},
        },
        validators=[MinSizeValidator(730, 410)],
    )

    description = MartorField()
    excerpt = models.TextField(blank=True, null=True)
    published_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    members_only = models.BooleanField(default=False)
    sent_on_social = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog-item", kwargs={"slug": self.slug})

    class Meta:
        ordering = ("-published_date",)


def blog_article_updated(sender, instance, **kwargs):
    if instance.active is False:
        return
    if instance.sent_on_social is True:
        return

    instance.sent_on_social = True
    instance.save()
    url = "https://%s%s" % (Site.objects.get_current().domain, instance.get_absolute_url())
    message = f"{instance.title} {url}"
    twitter_message.delay(message)
    matrix_message.delay(message)

post_save.connet(blog_article_updated, sender=Post)
