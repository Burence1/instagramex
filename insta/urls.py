from os import name
from django.conf import settings
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static

urlpatterns = [
  path('',views.index,name='home'),
  path('upload/',views.views.upload_post,name='NewPost'),
  path('update/',views.update_profile,name='UpdateProfile'),
  re_path('like/(?P<image_id>\d+)',views.like_post,name='LikePost'),
  path('create_profile/',views.create_profile,name='CreateProfile'),
  re_path('comment/(?P<image_id>\d+)',views.comment,name='AddComment'),
  re_path('profile/(?P<profile_id>\d+)',views.profile,name='UserProfile'),
  path('search/',views.search,name='Search'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)