from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from models import Article


class ArticleBaseView(View):

    def get_queryset(self):
        return super(ArticleBaseView, self).get_queryset().filter(site=self.request.site)


class ArticleListView(ArticleBaseView, ListView):
    model = Article


class ArticleDetailView(ArticleBaseView, DetailView):
    model = Article
