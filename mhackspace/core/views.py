from mhackspace.users.models import Membership
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from mhackspace.rfid.models import AccessLog


@method_decorator(cache_page(60 * 60 * 24), name="dispatch")
class ChatView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["open_graph"] = {
            "title": "Chat with us",
            "type": "website",
            "description": "Speak to members of the Hackspace directly.",
        }
        return context


@method_decorator(cache_page(60 * 60 * 24), name="dispatch")
class StatusView(TemplateView):
    template_name = "partials/status.html"

    def get_context_data(self, *args, **kwargs):
        membership_count = Membership.objects.filter(status=1).all().count()
        membership_expired = Membership.objects.filter(status=3).all().count()
        context = super().get_context_data(*args, **kwargs)
        context["members"] = membership_count
        context["members_expired"] = membership_expired

        access = AccessLog.objects.order_by("-access_date").first()
        context["space_access"] = {
            "user": access.rfid.user.username,
            "date": access.access_date,
        }
        return context


@method_decorator(cache_page(60 * 60 * 24), name="dispatch")
class AboutView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["open_graph"] = {
            "title": "About Us",
            "type": "article",
            "description": "Useful information about Maidstone Hackspace.",
        }
        return context
