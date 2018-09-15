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


class AboutView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["open_graph"] = {
            "title": "About Us",
            "type": "article",
            "description": "Useful information about Maidstone Hackspace.",
        }
        return context
