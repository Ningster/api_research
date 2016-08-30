from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import main

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'api_research.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', main),
    url(r'^admin/', include(admin.site.urls)),
)
