from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import main,search_FB_ID,search_yelp_category,name_match_id

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'api_research.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^search_FB_ID', search_FB_ID),
    url(r'^search_yelp_category', search_yelp_category),
    url(r'^name_match_id', name_match_id),
    url(r'^', main),
)
