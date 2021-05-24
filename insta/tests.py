from django.test import TestCase
from .models import Profile,Image,Comments,Follow
from django.contrib.auth.models import User

# Create your tests here.
class ImageTestClass(TestCase):
  def setUp(self):
    self.burens=User(username ='burens',email='burensdev@gmail.com',password='instagood')
    self.profile=Profile(bio='mybio',profile_image='imageurl',user=self.burens)
    self.tech = Image(image = 'imageurl', name ='tech', caption = 'tech', profile = self.profile)

    self.burens.save()
    self.profile.save()
    self.tech.save_image()

  def tearDown(self):
    Image.objects.all().delete()
  
  def test_instance(self):
    self.assertTrue(isinstance(self.tech, Image))

  def test_save_image(self):
    images=Image.objects.all()
    self.assertTrue(len(images),1)

  def test_delete_image(self):
    images=Image.objects.all()
    self.assertTrue(len(images),1)
    self.tech.delete_image()
    image=Image.objects.all()
    self.assertEqual(len(image),0)

  def test_update_image_caption(self):
    self.tech.update_caption("awesome")
    self.assertEqual(self.tech.caption, 'awesome')

  def test_profile_posts(self):
    images=Image.profile_images(self.profile)
    self.assertEqual(len(images),1)
  

# class ProfileTestClass(TestCase):
#   def SetUp(self):
#     self.burens=User(username ='burens',email='burensdev@gmail.com',password='instagood')
#     self.profile=Profile(bio='mybio',profile_image='imageurl',user=self.burens)
#     self.burens.save()

#   def tearDown(self):
#     Profile.objects.all().delete()
#     User.objects.all().delete()

#   def test_instance(self):
#     self.assertTrue(isinstance(self.burens, User))
#     self.assertTrue(isinstance(self.profile, Profile))

#   def test_search_profile(self):
#     user=Profile.search_profile(self.burens)
#     self.assertEqual(len(user), 1)

class CommentTestClass(TestCase):
  def setUp(self):
    self.burens=User(username ='burens',email='burensdev@gmail.com',password='instagood')
    self.profile=Profile(bio='mybio',profile_image='imageurl',user=self.burens)
    self.tech=Image(image = 'imageurl', name ='tech', caption = 'tech', profile = self.profile)
    self.comment=Comments(image=self.tech, comment='awesome',user=self.burens)

    self.burens.save()
    self.profile.save()
    self.tech.save()
    self.comment.save_comment()


  def tearDown(self):
    Image.objects.all().delete()
    Comments.objects.all().delete()

  def test_instance(self):
    self.assertTrue(isinstance(self.comment, Comments))

  def test_save_comment(self):
    self.comments = Comments(image=self.tech, user=self.burens, comment='test')
    self.comments.save_comment()
    comment = Comments.objects.all()
    self.assertTrue(len(comment),2)

  def test_delete_image(self):
    self.comments = Comments(image=self.tech, user=self.burens, comment='test')
    self.comments.save_comment()
    comments = Comments.objects.all()
    self.assertEqual(len(comments),2)
    self.comments.delete_comment()
    total_comments=Comments.objects.all()
    self.assertEqual(len(total_comments),1)

  def test_get_post(self):
    comments=Comments.get_post_comments(self.tech)
    self.assertEqual(len(comments),1)