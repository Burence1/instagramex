from django.test import TestCase
from .models import Profile,Image,Comments,Follow
from django.contrib.auth.models import User

# Create your tests here.
class TestProfile(TestCase):
  def SetUp(self):
    self.burens=User(username='burens',email='burensdev@gmail.com',password='aloha')
    self.profile=Profile(user=self.burens,bio='mybio',profile_image='image.url')
    self.vacation=Image(caption='alohalife',name='santorini',profile=self.profile,image='image.url')
    self.comment=Comments(coment='awesome',user=self.burens,image=self.vacation)

    self.burens.save()
    self.profile.save()
    self.vacation.save()
    self.comment.save()