import django.contrib.auth.views
from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.new, name='new'),
    url(r'^add/$', views.add, name='add'),
    url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'tracker/login.html'}, name='login'),
    url(r'^my/$', views.my, name='my'),
    url(r'^(?P<ticket_id>\d+)/$', views.ticket, name='ticket'),
    url(r'^(?P<ticket_id>\d+)/add_history/$', views.ticket_add_history, name='ticket_add_history'),
    url(r'^(?P<ticket_id>\d+)/add_me_to_cc/$', views.ticket_add_me_to_cc, name='ticket_add_me_to_cc'),
    url(r'^logout/$', views.logout_view, name='logout'),
)
