from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.core import serializers
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, date, time
import calendar
import math, decimal
from PIL import Image
from base64 import b64decode
from django.core.files.base import ContentFile
import json
from catalyst.models import *
import os
from django.conf import settings

# Create your views here.
def all_profiles_serialized(request):
	prof_set = []
	for prof in Profile.objects.all():
		prof_set.append({"pk":prof.pk, "info_blurb":prof.info_blurb, \
			"pic_url":'http://'+request.META['HTTP_HOST']+'/'+prof.photo.url})
		#for photos, url is relative - still need to add domain to front of string
	return HttpResponse(json.dumps(prof_set), content_type="application/json")

def nearby_profiles(request, username):
	prof_set = []
	user = Profile.objects.get(user__username = username)
	for prof in Profile.objects.filter(enabled = True).order_by('-user__last_login'):
		if (latlong_distance(user.latitude, user.longitude, prof.latitude, prof.longitude) < 100):
			prof_set.append({"pk":prof.pk, "info_blurb":prof.info_blurb, \
			"pic_url":'http://'+request.META['HTTP_HOST']+'/'+prof.photo.url})
		#for photos, url is relative - still need to add domain to front of string
	return HttpResponse(json.dumps(prof_set), content_type="application/json")

@csrf_exempt
def update_location(request):
	print "trying to update location for user"
	username = request.POST['username']
	print username, " got username"
	user = Profile.objects.get(user__username = username)
	user.latitude = decimal.Decimal(request.POST['userLatitude'])
	user.longitude = decimal.Decimal(request.POST['userLongitude'])
	print username, user.latitude, user.longitude
	user.save()
	json_data = json.dumps({"update_status": "success"})
	return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def edit_info_blurb(request):
	print "user is trying to edit info blurb"
	username1 = request.POST['username']
	ib = request.POST['edit_blurb']
	print "username is = ", username1
	prof = Profile.objects.get(user__username = username1)
	prof.info_blurb = ib
	prof.save()
	json_data = json.dumps({"edit_blurb": "success"})
	return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def change_status(request, username, status):
	prof = Profile.objects.get(user__username = username)
	print "the status from the url is ", status
	if status == "disable":
		prof.enabled = False
		print "changed profile is_active to ", prof.user.is_active
	elif status == "enable":
		prof.enabled = True
		print "changed profile is_active to ", prof.user.is_active
	prof.save()
	print "the current is_active is ", prof.user.is_active
	json_data = json.dumps({"status": "success"})
	return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def get_user_info(request, username):
	prof = Profile.objects.get(user__username = username)
	json_data = json.dumps({"pk":prof.pk, "info_blurb":prof.info_blurb, \
		"pic_url":'http://'+request.META['HTTP_HOST']+'/'+prof.photo.url, \
		"status":str(prof.enabled)})
	return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def edit_pic(request):
        print "user is trying to edit profile pic"
        username1 = request.POST['username']
        img = request.POST['image']
        prof = Profile.objects.get(user__username=username1)
        #Check if profile photo file already exists, if it does, delete it
        #before saving new photo of the same name
        fullname = os.path.join(settings.MEDIA_ROOT[:-6], prof.photo.url)
        if os.path.exists(fullname):
                os.remove(fullname)
        prof.photo = ContentFile(b64decode(img), prof.user.username+'_'+calendar.timegm(time.gmtime())+'.jpg')
        prof.save()
        json_data = json.dumps({"edit_pic":"success"})
        return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def register_user(request):
	print "user is trying to register"
	username1 = request.POST['username']
	password1 = request.POST['password']
	lat = request.POST['userLatitude']
	longi = request.POST['userLongitude']
	ib = request.POST['blurb']
	img = request.POST['image']
	registration = ''
	if User.objects.filter(username=username1).count():
		registration = 'user_exists'
	else:
		print "username does not exist, attempting to register user"
		u = User(username=username1)#, email=em)
		u.set_password(password1)
		u.save()
		prof = Profile(info_blurb = ib, pub_date = datetime.now(), user = u)
		prof.latitude = lat
		prof.longitude = longi
		print 'attempting to save image to directory'
		img_filename = prof.user.username + '.jpg'
		prof.photo = ContentFile(b64decode(img), img_filename)
		prof.save()
		user = authenticate(username=username1, password=password1)
	
	if registration is '':
		if user is not None:
			registration= 'success'
		else:
			registration= 'failure'
	json_data = json.dumps({"registration":registration})
	print json_data
	return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def authenticate_user(request):
	print "user is trying to authenticate"
	username1 = request.POST['username']
	password1 = request.POST['password']
	lat = request.POST['userLatitude']
	longi = request.POST['userLongitude']
	user = authenticate(username=username1, password=password1)
	authentication = ''
	if user is not None:
		if user.is_active:
			login(request, user)
			# Redirect to a success page.
			print "user was found in the database, login successfull"
			authentication = 'success'
		else:
			# Return a 'disabled account' error message
			print "somehow user was found to be disabled"
			authentication = 'failure'
	else:
		# Return an 'invalid login' error message.
		print "user was not found in database"
		authentication = 'failure'
	
	#Set user latitude and longitude
	prof = Profile.objects.get(user__username = username1)
	prof.latitude = lat
	prof.longitude = longi
	prof.save()
	json_data = json.dumps({"authentication": authentication})
	print json_data
	return HttpResponse(json_data, content_type="application/json")

def latlong_distance(lat1, long1, lat2, long2):
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0
	# phi = 90 - latitude
	phi1 = (decimal.Decimal(90.0) - lat1)*decimal.Decimal(degrees_to_radians)
	phi2 = (decimal.Decimal(90.0) - lat2)*decimal.Decimal(degrees_to_radians)
	# theta = longitude
	theta1 = long1*decimal.Decimal(degrees_to_radians)
	theta2 = long2*decimal.Decimal(degrees_to_radians)
	# Compute spherical distance from spherical coordinates.
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
	arc = math.acos( cos )
	arc = decimal.Decimal(arc) * decimal.Decimal(20925524.9)
	return arc