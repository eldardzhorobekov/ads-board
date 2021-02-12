# from django.test import TestCase, override_settings
# from django.contrib.auth import get_user_model
# from django.forms import modelformset_factory

# from ad.forms import AdvertisementForm, AdvertisementImageForm
# from ad.helpers import get_test_image
# from ad.models import Category, Advertisement, AdvertisementImage, City 

# class AdvertisementFormTest(TestCase):

#     def setUp(self):
#         self.city1 = City.objects.create(city='Bishkek')
#         self.category1 = Category.objects.create(
#             title='Category 1',
#             parent=None
#         )
#         self.form_data = {
#             'description': 'This is test desciption',
#             'price': 1000,
#             'currency': Advertisement.Currency.SOM,
#             'city': self.city1,
#             'category': self.category1,
#             'phone_number': '+996777991122',
#             'hide_phone_number': True,
#             'email': 'example@google.com',
#         }
#         self.form_files = {'main_image': get_test_image()}


#     def test_advertisement_form(self):
#         adv_form = AdvertisementForm(data=self.form_data, files=self.form_files)
#         self.assertTrue(adv_form.is_valid())

#     def test_advertisement_images_form(self):
#         ImageFormSet = modelformset_factory(AdvertisementImage, form=AdvertisementImageForm, extra=3)
#         formset = ImageFormSet({
#             'form-TOTAL_FORMS': '2',
#             'form-INITIAL_FORMS': '0',
#             'form-0-image': get_test_image(),
#             'form-1-image': get_test_image()
#             })
#         self.assertTrue(formset.is_valid())

#     def tearDown(self):
#         pass