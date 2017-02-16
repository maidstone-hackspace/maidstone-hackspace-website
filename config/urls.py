# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.auth import views as auth_views

from mhackspace.contact.views import contact
from mhackspace.members.views import MemberListView
from mhackspace.subscriptions import views as subscription
from mhackspace.base.feeds import LatestEntriesFeed
from mhackspace.blog.feeds import BlogFeed, BlogCategoryFeed

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^chat/$', TemplateView.as_view(template_name='pages/chat.html'), name='chat'),
    url(r'^mailing-list/$', TemplateView.as_view(template_name='pages/mailing-list.html'), name='group'),

    url(r'^contact/$', contact, name='contact'),
    url(r'^blog/$', contact, name='contact'),
    url(r'^blog/rss/$', BlogFeed()),
    url(r'^blog/(?P<slug>[0-9A-Za-z_\-]+)/$', BlogCategoryFeed(), name='blog-item'),
    url(r'^blog/category/(?P<slug>[0-9A-Za-z_\-]+)/$', BlogCategoryFeed(), name='blog-category'),
    url(r'^blog/category/(?P<category>[0-9A-Za-z_\-]+)/rss/$', BlogCategoryFeed(), name='blog-category_feed'),


    # need to be logged in for these urls
    url(r'^members/$', MemberListView.as_view(), name='members'),

    # Django Admin, use {% url 'admin:index' %}
    url(r'{}'.format(settings.ADMIN_URL), admin.site.urls),

    # User management
    url(r'^users/', include('mhackspace.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^latest/$', LatestEntriesFeed()),

    url(r'membership/join/$', subscription.MembershipJoinView.as_view(), name='join_hackspace'),
    url(r'membership/(?P<provider>[\w\-]+)/success$', subscription.MembershipJoinSuccessView.as_view(), name='join_hackspace_success'),
    url(r'membership/(?P<provider>\w{0,50})/failure$', subscription.MembershipJoinFailureView.as_view(), name='join_hackspace_failure'),
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]
