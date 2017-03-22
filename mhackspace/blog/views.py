from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView
from rest_framework import viewsets
from django_filters import DateTimeFromToRangeFilter
from django_filters.rest_framework import FilterSet
from django_filters.widgets import RangeWidget
from mhackspace.blog.models import Post, Category
from mhackspace.blog.serializers import PostSerializer, CategorySerializer


class BlogPost(DetailView):
    context_object_name = 'post'
    queryset = Post.objects.filter(active=True, members_only=False)  # todo: check member status here


class PostList(ListView):
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        if 'category' in self.kwargs:
            self.category = get_object_or_404(Category, slug=self.kwargs['category'])
            return Post.objects.filter(active=True, categories=self.category, published_date__lte=timezone.now(), members_only=False)
        return Post.objects.filter(active=True, published_date__lte=timezone.now(), members_only=False)


class PostFilter(FilterSet):
    published_date = DateTimeFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'dd/mm/yyyy hh:mm'}))
    updated_date = DateTimeFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'dd/mm/yyyy hh:mm'}))

    class Meta:
        model = Post
        fields = ('title', 'slug', 'author__name', 'published_date', 'updated_date')


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(active=True)
    filter_class = PostFilter
    serializer_class = PostSerializer
    search_fields = ('title', 'slug', 'categories', 'author__name')
    ordering_fields = ('title', 'published_date', 'updated_date', 'author')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name', 'slug')
    ordering_fields = ('name', 'slug')
    filter_fields = ('name', 'slug')
