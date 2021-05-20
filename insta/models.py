from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.fields import DateField

# Create your models here.
class Images(models.Model):
  image = CloudinaryField('photo')
  caption=models.TextField(blank=True)
  name=models.CharField(max_length=30)
  pub_date=models.DateField(auto_now_add=True)
  
  