from django.conf.urls import patterns, url

from catalyst import views
urlpatterns = patterns('',
	url(r'^all_profiles_serialized/$', views.all_profiles_serialized, name='all_infographics_serialized'),
	url(r'^nearby_profiles/(?P<username>\w{0,50})/$', views.nearby_profiles,),
	url(r'^update_location/$', views.update_location,),
	url(r'^login/$', views.authenticate_user, name='user_authentication'),
	url(r'^register/$', views.register_user, name='user_registration'),
	url(r'^edit_info_blurb/$', views.edit_info_blurb, name='user_edit_blurb'),
	url(r'^edit_pic/$', views.edit_pic, name='user_edit_prof_pic'),
	url(r'^user/(?P<username>\w{0,50})/$', views.get_user_info,),
	url(r'^user/(?P<username>\w{0,50})/(?P<status>(enable|disable))/$', views.change_status,)
	)