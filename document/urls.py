from django.conf.urls import url
from .views import *

app_name = 'document'

urlpatterns = [
    url(r'^create/$', DocumentCreateView.as_view(success_url="/docs"), name='create'),
    url(
        regex=r'^$',
        view=DocumentListView.as_view(),
        name='list'
    ),
    url(
        regex=r'^(?P<pk>\d+)/$',
        view=DocumentDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^(?P<pk>\d+)/edit/$',
        view=DocumentUpdateView.as_view(),
        name='edit'
    ),
    url(r'json_docs', json_docs, name='json_docs'),
]
