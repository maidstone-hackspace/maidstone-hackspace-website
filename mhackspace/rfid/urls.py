from django.conf.urls import url

from mhackspace.rfid import views

access_card_patterns = ([
    url(
      regex=r'^$',
      view=views.RfidCardsListView.as_view(),
      name='index'
    ),
    url(
      regex=r'^create$',
      view=views.RfidCardsUpdateView.as_view(),
      name='create'
    ),
    url(
      regex=r'^delete/(?P<pk>\d+)/$',
      view=views.RfidCardsDeleteView.as_view(),
      name='delete'
    ),
], 'access_cards')
