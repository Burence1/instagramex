from os import name
from django.conf import settings
from django.urls import path,re_path
from . import views
from django.conf.urls.static import static

urlpatterns = [
  path('',views.index,name='home'),
  path('upload/',views.views.upload_post,name='NewPost'),
  path('update/',vie)
]