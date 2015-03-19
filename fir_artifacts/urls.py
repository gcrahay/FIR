from django.conf.urls import patterns, url

from fir_artifacts import views

urlpatterns = patterns('',
	url(r'^(?P<event_id>\d+)/list', views.list, name='list'),
    url(r'^(?P<event_id>\d+)/correlation', views.correlation, name='correlation'),
	#url(r'^(?P<event_id>\d+)/new', views.new, name='new'),
	#url(r'^edit/(?P<nugget_id>\d+)', views.edit, name='edit'),
	#url(r'^delete/(?P<nugget_id>\d+)', views.delete, name='delete'),
)
