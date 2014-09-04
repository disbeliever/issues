from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'issues.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    url(r'^tracker/', include('tracker.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
