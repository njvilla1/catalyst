from django.conf.urls import patterns, url

from catalyst import views
urlpatterns = patterns('',
	#url(r'^$', views.index, name = 'index'),
	url(r'^all_profiles_serialized/$', views.all_profiles_serialized, name='all_infographics_serialized'),
	url(r'^login/$', views.authenticate_user, name='user_authentication'),
	url(r'^register/$', views.register_user, name='user_registration'),
	)
