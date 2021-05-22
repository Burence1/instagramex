from django.db import models
from .models import Image,Follow,Profile,Comments
from django.forms import  ModelForm

class FollowForm(ModelForm):
  class Meta:
    model = Follow
    exclude = ['followed','follower']

class UnfollowForm(ModelForm):
  class Meta:
    model = Follow
    exclude = ['followed','follower']

class CreateProfileForm(ModelForm):
  class Meta:
    model = Profile
    exclude = ['followers','following']

class UpdateProfile(ModelForm):
  class Meta:
    model = Profile
    fields = ['bio','profile_image']