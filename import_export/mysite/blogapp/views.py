from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
from django.contrib.syndication.views import Feed

from .models import Article
    

class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .filter(published_at__isnull=False)
        .order_by("-published_at")
    )


class ArticleDetailView(DetailView):
    model = Article



class LatestArticlesFeed(Feed):
    title = "Blog articles (latest)"
    description = "Updates on change and addition blog articles"
    link = reverse_lazy("blogapp:articles")

    def items(self):
        return (
            Article.objects
            .filter(published_at__isnull=False)
            .order_by("-published_at")[:5]
        )
    
    def item_description(self, item: Article):
        return item.body[:200]
    
    def item_link(self, item: Article):
        return reverse("blogapp:article", kwargs={"pk": item.pk})