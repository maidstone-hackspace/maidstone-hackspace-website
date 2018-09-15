# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from mhackspace.contact.views import contact
from mhackspace.members.views import MemberListView
from mhackspace.subscriptions import views as subscription
from mhackspace.base.feeds import LatestEntriesFeed
from mhackspace.blog.feeds import RssFeed, BlogFeed, BlogCategoryFeed
from mhackspace.base.views import markdown_uploader
from mhackspace.blog.views import PostViewSet, CategoryViewSet, BlogPost, PostList
from mhackspace.blog.sitemaps import PostSitemap, CategorySitemap
from mhackspace.feeds.views import FeedViewSet, ArticleViewSet
from mhackspace.requests.views import RequestsForm, RequestsList, RequestsDetail, RequestsDetailForm
from mhackspace.rfid.views import DeviceViewSet, AuthUserWithDeviceViewSet
from mhackspace.core.views import ChatView, AboutView

from mhackspace.register.views import RegisterForm
from mhackspace.wiki.urls import CustomWikiUrlPatterns

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()
router.register(r'posts', PostViewSet, 'posts')
router.register(r'categories', CategoryViewSet, base_name='categories')
router.register(r'feeds', FeedViewSet, 'feeds')
router.register(r'articles', ArticleViewSet, base_name='articles')
router.register(r'rfid', DeviceViewSet, base_name='rfid_device')
router.register(r'rfidAuth', AuthUserWithDeviceViewSet, base_name='device_auth')


sitemaps = {
    'posts': PostSitemap,
    'category': CategorySitemap,
}


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', AboutView.as_view(template_name='pages/about.html'), name='about'),
    url(r'^chat/$', ChatView.as_view(template_name='pages/chat.html'), name='chat'),
    url(r'^mailing-list/$', TemplateView.as_view(template_name='pages/mailing-list.html'), name='group'),
    url(r'^contact/$', contact, name='contact'),

    url(r'^requests/$', RequestsList.as_view(), name='requests'),
    url(r'^requests/create$', RequestsForm.as_view(), name='requests_form'),
    url(
        r'^requests/(?P<pk>\d+)/$',
        RequestsDetail.as_view(template_name='pages/requests-detail.html'),
        name='requests_detail'),
    url(r'^requests/(?P<pk>\d+)/submit/$', RequestsDetailForm.as_view(template_name='pages/requests-detail.html'), name='requests_detail_form'),

    url(r'^discuss/', include(('spirit.urls', 'spirit'), namespace='spirit')),
    url(r'^api/v1/', include((router.urls, 'v1'), namespace='v1')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^martor/', include('martor.urls')),
    url(
        r'^api/uploader/$',
        markdown_uploader, name='markdown_uploader_page'
    ),
    url(r'^blog/$', PostList.as_view(), name='blog'),
    url(r'^blog/rss/$', BlogFeed(), name='blog-rss'),
    url(r'^rss.xml$', RssFeed(), name='main-rss'),
    url(r'^blog/(?P<slug>[0-9A-Za-z_\-]+)/$', BlogPost.as_view(), name='blog-item'),
    url(r'^blog/category/(?P<category>[0-9A-Za-z_\-]+)/$', PostList.as_view(), name='blog-category'),
    url(r'^blog/category/(?P<category>[0-9A-Za-z_\-]+)/rss/$', BlogCategoryFeed(), name='blog-category-feed'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    # need to be logged in for these urls
    url(r'^members/$', MemberListView.as_view(), name='members'),
    url(r'^members/(?P<status>[a-zA-Z]+)/$', MemberListView.as_view(), name='members_status'),

    # Django Admin, use {% url 'admin:index' %}
    url(r'{}'.format(settings.ADMIN_URL), admin.site.urls),

    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api/docs/', include_docs_urls(title='Hackspace API')),

    # User management
    url(r'^users/', include(('mhackspace.users.urls', 'users'), namespace='users')),
    url(r'^accounts/', include('allauth.urls')),
    url('^accounts/', include('django.contrib.auth.urls')),

    # Your stuff: custom urls includes go here
    url(r'^latest/$', LatestEntriesFeed()),

    url(r'membership/join/$', subscription.MembershipJoinView.as_view(), name='join_hackspace'),
    url(r'membership/cancel/$', subscription.MembershipCancelView.as_view(), name='cancel_membership'),
    url(r'membership/(?P<provider>[\w\-]+)/success$', subscription.MembershipJoinSuccessView.as_view(), name='join_hackspace_success'),
    url(r'membership/(?P<provider>\w{0,50})/failure$', subscription.MembershipJoinFailureView.as_view(), name='join_hackspace_failure'),
    url(r'^admin/password_reset/$', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    url(r'^register/$', RegisterForm.as_view(), name='register_form'),
    url(r'^register/success$', TemplateView.as_view(template_name='pages/register.html'), name='register_success'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^notifications/', get_nyt_pattern()),
    url(r'^wiki/', get_wiki_pattern(url_config_class=CustomWikiUrlPatterns), name='wiki')
]
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
