from django.contrib import admin
from catalyst.models import *

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('prof_id', 'user', 'pub_date', 'latitude', 'longitude')

# Register your models here.
admin.site.register(Profile, ProfileAdmin)