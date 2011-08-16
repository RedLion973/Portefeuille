from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from FUTFactory.utils.views import HomeView, ReportView, rasterize

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(template_name="index.html"), name="home"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/', 'redirect_field_name': 'redirect_to'}, name="logout"),
    url(r'^futs-mangement/', include('FUTFactory.fut.urls')),
    url(r'^report/$', login_required(ReportView.as_view(template_name="report.html")), name="report"),
    url(r'^rasterize/$', rasterize),
    url(r'^admin/', include(admin.site.urls)),
)
