from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from rest_framework import viewsets
from django_filters import DateTimeFromToRangeFilter
from django_filters.rest_framework import FilterSet
from django_filters.widgets import RangeWidget
from mhackspace.blog.models import Post, Category
from mhackspace.blog.serializers import PostSerializer, CategorySerializer


def blog(request, slug=None, category=None):
    categories = Category.objects.all()

    if slug is not None:
        blog_posts = Post.objects.filter(active=True, slug=slug)
    elif category is not None:
        category = Category.objects.filter(slug=category)
        blog_posts = Post.objects.filter(active=True, categories=category, published_date__lte=timezone.now())
    else:
        blog_posts = Post.objects.filter(active=True, published_date__lte=timezone.now())

    if len(blog_posts) < 1:
        raise Http404("No posts found")

    paginator = Paginator(blog_posts, 5)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/posts.html', {'posts': posts, 'categories': categories})


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
