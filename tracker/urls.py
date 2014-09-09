from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^add/$', views.add, name='add'),
    url(r'^login/$', views.login, name='login'),
    url(r'^my/$', views.my, name='my'),
    url(r'^(?P<ticket_id>\d+)/$', views.ticket, name='ticket'),
)
