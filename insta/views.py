from django import forms
from django.http.response import Http404
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,Http404
from .models import Profile,Follow,Image,Comments
from django.contrib.auth.models import User
from .forms import UnfollowForm,FollowForm,CreateProfileForm,UpdateProfile,CreatePost

# Create your views here.
def index(request):
  current_user=request.user
  try:
    profile= Profile.objects.get(user=current_user)
  except Profile.DoesNotExist:
    raise Http404()

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
      raise Http404()
    current_user=request.user
    try:
      profile=Profile.objects.get(id=user_id)
    except Profile.DoesNotExist:
      raise Http404()

    try:
      prof_follower=Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
      raise Http404()
    try:
      prof_followed=Profile.objects.get(user=current_user)
    except Profile.DoesNotExist:
      raise Http404()

    if request.method == 'POST':
      if 'follow' in request.POST:
        form = FollowForm(request.POST)
        if form.is_valid():
          new_followed=form.save(commit=False)
          new_followed.followed=prof_followed
          new_followed.follower=prof_follower
          new_followed.save()
          user_following=Follow.objects.filter(followed=prof_followed)
          following_stats=len(user_following)
          prof_followed.following=following_stats
          prof_followed.save()

          user_followers=Follow.objects.filter(follower=prof_follower)
          followers_stats=len(user_followers)
          prof_follower.followers=followers_stats
          prof_follower.save()
          
        return HttpResponseRedirect()

      elif 'unfollow' in request.POST:
        form = UnfollowForm(request.POST)
        if form.is_valid():
          new_unfollow=form.save(commit=False)
          new_unfollow.followed = prof_followed
          new_unfollow.follower = prof_follower
          new_unfollow.delete()

          user_following=Follow.objects.filter(followed=prof_followed)
          following_stats=len(user_following)
          prof_followed.following=following_stats
          prof_followed.save()

          user_followers=Follow.objects.filter(follower=prof_follower)
          followers_stats=len(user_followers)
          prof_follower.followers=followers_stats
          prof_follower.save()

        return HttpResponseRedirect()

    else:
      follow_form=FollowForm()
      unfollow_form=UnfollowForm()

    images=Image.profile_images(profile=profile).order_by('-pub_date')

    post=len(images)

    is_following=Follow.objects.filter(followed=prof_followed,follower=prof_follower)

    if is_following:
      return render(request,'profile/profile.html',{"profile":profile,"post":post,"images":images,"unfollow_form":unfollow_form})
    return render(request,'profile/profile.html',{"profile":profile,"images":images,"post":post,"follow_form":follow_form,})

  else:
    not_searched="No user searched"
    return render(request,'profile/profile.html',{"not_searched":not_searched})

def profile(request,profile_id):
  current_user = request.user
  try:
    profile=Profile.objects.get(id=profile_id)
  except Profile.DoesNotExist:
    raise Http404()

  try:
    prof_follower=Profile.objects.get(user=current_user)
  except Profile.DoesNotExist:
    raise Http404()
  try:
    prof_followed=Profile.objects.get(user=current_user)
  except Profile.DoesNotExist:
    raise Http404()

  if request.method == 'POST':
    if 'follow' in request.POST:
      form = FollowForm(request.POST)
      if form.is_valid():
        new_followed=form.save(commit=False)
        new_followed.followed=prof_followed
        new_followed.follower=prof_follower
        new_followed.save()
        user_following=Follow.objects.filter(followed=prof_followed)
        following_stats=len(user_following)
        prof_followed.following=following_stats
        prof_followed.save()

        user_followers=Follow.objects.filter(follower=prof_follower)
        followers_stats=len(user_followers)
        prof_follower.followers=followers_stats
        prof_follower.save()
        
      return HttpResponseRedirect()

    elif 'unfollow' in request.POST:
      form = UnfollowForm(request.POST)
      if form.is_valid():
        new_unfollow=form.save(commit=False)
        new_unfollow.followed = prof_followed
        new_unfollow.follower = prof_follower
        new_unfollow.delete()

        user_following=Follow.objects.filter(followed=prof_followed)
        following_stats=len(user_following)
        prof_followed.following=following_stats
        prof_followed.save()

        user_followers=Follow.objects.filter(follower=prof_follower)
        followers_stats=len(user_followers)
        prof_follower.followers=followers_stats
        prof_follower.save()

      return HttpResponseRedirect()

  else:
    follow_form=FollowForm()
    unfollow_form=UnfollowForm()

  images=Image.profile_images(profile=profile).order_by('-pub_date')

  post=len(images)

  is_following=Follow.objects.filter(followed=prof_followed,follower=prof_follower)

  if is_following:
    return render(request,'profile/profile.html',{"profile":profile,"post":post,"images":images,"unfollow_form":unfollow_form})
  return render(request,'profile/profile.html',{"profile":profile,"images":images,"post":post,"follow_form":follow_form,})


def comment(request,image_id):
  image=Image.objects.get(pk_in=image_id)
  comments=Comments.objects.GET.get("comments")
  current_user=request.user
  comment=Comments(image=image,comment=comments,user=current_user)
  comment.save_comment()

  return redirect('home')

def create_profile(request):
  current_user=request.user
  if request.method == 'POST':
    form = CreateProfileForm(request.POST,request.FILES)
    if form.is_valid():
      profile = form.save(commit=False)
      profile.user = current_user
      profile.save()
    return HttpResponseRedirect('/')
  else:
    form = CreateProfileForm()
    return render(request,'create-profile.html',{"form":form})

def like_post(request,image_id):
  image = Image.objects.get(pk=image_id)
  is_liked=False
  user=request.user
  try:
    profile=Profile.objects.get(user=user)
  except Profile.DoesNotExist:
    raise Http404()
  if image.likes.filter(id=profile.id).exists():
    image.likes.remove(profile)
    is_liked=False
  else:
    image.likes.add(profile)
    is_liked=True
  return HttpResponseRedirect('home')
  
def update_profile(request):
  user=request.user
  if request.method == 'POST':
    form=UpdateProfile(request.POST,request.FILES)
    if form.is_valid():
      profile_image = form.cleaned_data['profile_image']
      bio = form.cleaned_data['bio']
      update_prof=Profile(profile_image=profile_image,bio=bio,user=user)
      update_prof.save()
    return redirect('profile')
  else:
    form = UpdateProfile()
  return render(request, 'update_prof.html',{"form":form})

def upload_post(request):
  user=request.user
  try:
    profile=Profile.objects.get(user=user)
  except Profile.DoesNotExist:
    raise Http404()
  if request.methods == 'POST':
    form = CreatePost(request.POST,request.FILES)
    if form.is_valid():
      new_post=form.save(commit=False)
      new_post.profile = profile
      new_post.save()
    return redirect('home')
  else:
    form = CreatePost()
  return render(request,'create_post.html',{"form":form})