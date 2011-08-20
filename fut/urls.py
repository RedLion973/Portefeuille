from django.conf.urls.defaults import patterns, url
from FUTFactory.fut.views import FUTDetailView, FUTListView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^futs/page-(?P<page>\d+)/$', login_required(FUTListView.as_view()), name='futs-index'),
    url(r'^futs/(?P<pk>\d+)/$', login_required(FUTDetailView.as_view()), name='fut-detail'),                       
)