from django.conf.urls import patterns, url

from .views import ItemDetailView

urlpatterns = patterns(
    '',
    url(r'item/(?P<pk>\d+)/$', ItemDetailView.as_view(), name='item'),
)
