from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mhackspace.blog.models import Post, Category

def blog(request, slug=None, category=None):
    categories = Category.objects.all()

    try:
        if slug is not None:
            blog_posts = Post.objects.filter(slug=slug)
        elif category is not None:
            category = Category.objects.filter(slug=category)
            blog_posts = Post.objects.filter(categories=category)
        else:
            blog_posts = Post.objects.all()
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    paginator = Paginator(blog_posts, 5)

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/posts.html', {'posts': posts, 'categories': categories})
