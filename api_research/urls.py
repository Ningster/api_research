from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import main,search_FB_ID,search_yelp_term

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'api_research.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search_FB_ID', search_FB_ID),
    url(r'^search_yelp_term', search_yelp_term),
    url(r'^', main),
)
