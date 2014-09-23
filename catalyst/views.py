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
		prof_set.append({"pk":prof.pk, "info_blurb":prof.info_blurb, "pic_url":'http://'+request.META['HTTP_HOST']+'/'+prof.photo.url})
		#for photos, url is relative - still need to add domain to front of string
	return HttpResponse(json.dumps(prof_set))

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
def get_user_info(request, username):
	prof = Profile.objects.get(user__username = username)
	json_data = json.dumps({"pk":prof.pk, "info_blurb":prof.info_blurb, "pic_url":'http://'+request.META['HTTP_HOST']+'/'+prof.photo.url})
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

        prof.photo = ContentFile(b64decode(img), prof.user.username+'.jpg')
        prof.save()
        json_data = json.dumps({"edit_pic":"success"})
        return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def register_user(request):
	print "user is trying to register"
	username1 = request.POST['username']
	password1 = request.POST['password']
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
		prof = Profile(info_blurb = ib, pub_date = datetime.now(), user = u) #, photo = ...)
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
	print registration
	json_data = json.dumps({"registration":registration})
	
	return HttpResponse(json_data, content_type="application/json")

@csrf_exempt
def authenticate_user(request):
	print "user is trying to authenticate"
	username1 = request.POST['username']
	password1 = request.POST['password']
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
	
	json_data = json.dumps({"authentication": authentication})
	
	return HttpResponse(json_data, content_type="application/json")



