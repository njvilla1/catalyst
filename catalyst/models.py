from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(User, null=True) 
	info_blurb = models.CharField(max_length=250, default="default text")
	photo = models.ImageField(upload_to='catalyst/profile_photos', null=True)
	pub_date = models.DateTimeField('date published')
	latitude = models.DecimalField(max_digits=11, decimal_places=8)
	longitude = models.DecimalField(max_digits=11, decimal_places=8)	
	def __str__(self):
		return str(self.pk) + '_' + str(self.user.username)
	def prof_id(self):
		return "%09d" % (self.pk, )
