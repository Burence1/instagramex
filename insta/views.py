from django.http.response import Http404
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,Http404
from .models import Profile,Follow,Image,Comments
from django.contrib.auth.models import User

# Create your views here.
def index(request):
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

    timeline_images=Image.objects.filter(pk__in=index_timeline).order_by('-pub_date')
    like_image=False
    for image in timeline_images:
      images=Image.objects.get(pk=image.id)
      like_image=False
      if image.likes.filter(pk__in=index_timeline).order('-pub_date'):
        like_image= True

    image_comments=Comments.objects.all()[:4]
    total_comments=Comments.objects.all()
    count=len(total_comments)
    follow_suggestions=Profile.objects.all()[:6]
    title = "Instagramex"

    return render(request,'index.html',{"title":title,"profile":profile,"timeline_images":timeline_images,"image_comments":image_comments,"follow_suggestions":follow_suggestions,"like_image":like_image,"count":count})


def search(request):
  if 'user' in request.GET and request.GET['user']:
    searched_profile=request.GET.get("user")
    try:
      user=Profile.search_profile(searched_profile).first()
      user_id=user

    except User.DoesNotExist:
      raise Http404
    current_user=request.user
    try:
      profile=Profile.objects.get(id=user_id)
    except Profile.DoesNotExist:
      raise Http404

    try:
      prof_following=Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
      raise Http404
    try:
      prof_followed=Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
      raise Http404
      