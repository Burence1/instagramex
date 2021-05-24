from django.test import TestCase
from .models import Profile,Image,Comments,Follow
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTestClass(TestCase):
  def SetUp(self):
    self.burens=User(username='burens',email='burensdev@gmail.com',password='aloha')
    self.profile=Profile(user=self.burens,bio='mybio',profile_image='image.url')
    self.burens.save()
    self.profile.save()

  def tearDown(self):
    Profile.objects.all().delete()
    User.objects.all().delete()

  def test_instance(self):
    self.assertTrue(isinstance(self.burens, User))
    self.assertTrue(isinstance(self.profile, Profile))

  def test_search_profile(self):
    user=Profile.search_profile(self.burens)
    self.assertEqual(len(user), 1)