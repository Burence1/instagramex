from django.http.response import Http404
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,Http404
from .models import Profile,Follow,Image,Comments
from django.contrib.auth.models import User

# Create your views here.
def index(request):
  title="Instagramex"
  current_user=request.user
  try:
    profile= Profile.objects.get(user=current_user)
  except Profile.DoesNotExist:
    raise Http404

  index_timeline=[]
  images = Image.profile_images(profile=profile)
  for image in images:
    index_timeline.append(image.id)

  followers_posts=Follow.objects.filter(follower=profile)
  for follower in followers_posts:
    followed_profiles=follower.followed
    followed_images=Image.profile_images(followed_profiles)
    for images in followed_images:
      index_timeline.append(images.id)