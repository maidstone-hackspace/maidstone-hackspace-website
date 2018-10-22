from wiki.views.article import ArticleView


class WikiArticleView(ArticleView):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["open_graph"] = {
            "image": "", # self.article.image,
            "title": self.article.current_revision.title,
            "type": "article",
            "description": self.article.current_revision.content,
        }
        return context
