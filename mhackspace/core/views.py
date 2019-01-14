from mhackspace.users.models import Membership
from django.views.generic import TemplateView



class ChatView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["open_graph"] = {
            "title": "Chat with us",
            "type": "website",
            "description": "Speak to members of the Hackspace directly.",
        }
        return context


class StatusView(TemplateView):
    template_name = "partials/status.html"

    def get_context_data(self, *args, **kwargs):
        membership_count = Membership.objects.all().count()
        context = super().get_context_data(*args, **kwargs)
        context["members"] = membership_count
        context["atspace"] = membership_count
        return context


class AboutView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["open_graph"] = {
            "title": "About Us",
            "type": "article",
            "description": "Useful information about Maidstone Hackspace.",
        }
        return context
