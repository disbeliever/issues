from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^(?P<ticket_id>\d+)/$', views.ticket, name='ticket'),
)
