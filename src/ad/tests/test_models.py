# from django.test import TestCase, override_settings
# from django.conf import settings
# from django.core.files import File
# from django.contrib.auth import get_user_model

# import mock
# import tempfile
# from shutil import rmtree

# from ad.helpers import get_test_image
# from ad.models import \
#     Category, Advertisement, \
#     AdvertisementImage, City

# User = get_user_model()

# class CategoryTest(TestCase):
#     def setUp(self):
#         self.category1 = Category.objects.create(
#             title='Category 1',
#             parent=None
#         )
#         self.category2 = Category.objects.create(
#             title='Категория 2',
#             parent=self.category1
#         )

#     def test_category_slug_assigned_on_creation(self):
#         self.assertEquals(self.category1.slug, 'category-1')
#         self.assertEquals(self.category2.slug, 'kategoriya-2')
        

# class AdvertisementTest(TestCase):
#     def setUp(self):
#         self.user1 = User.objects.create(email='example@gmail.com', password='strongpassword1!')
#         self.category1 = Category.objects.create(
#             title='Category 1',
#             parent=None
#         )
#         self.city1 = City.objects.create(
#             city='Bishkek'
#         )
#         self.adv1 = Advertisement.objects.create(
#             description='This is test advertisement',
#             category=self.category1,
#             price=1000,
#             currency='SOM',
#             city=self.city1,
#             phone_number='+996772828809',
#             email='example@google.com',
#             hide_phone_number=False,
#             author=self.user1
#         )
#         self.image1 = AdvertisementImage.objects.create(
#             advertisement=self.adv1,
#             image=get_test_image()
#         )
    
#     def test_image_created(self):
#         self.assertEqual(AdvertisementImage.objects.count(), 1)
#         self.assertEqual(Advertisement.objects.count(), 1)

#     def tearDown(self):
#         # delete images in media folder with django-cleanup
#         self.adv1.delete()
#         self.image1.delete()

