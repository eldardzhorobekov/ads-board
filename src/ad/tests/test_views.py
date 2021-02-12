from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

import shutil

from ad.helpers import get_test_image
from ad.forms import AdvertisementForm
from ad.models import Category, Advertisement, \
    AdvertisementImage, City


CustomUser = get_user_model()

class CategoryTest(TestCase):
    def setUp(self):
        self.category1 = Category.objects.create(
            title='category1',
            parent=None
        )
        self.category2 = Category.objects.create(
            title='Категория2',
            parent=self.category1
        )

    def test_category_GET(self):
        response = self.client.get(reverse('ads:category', args=['category1']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/category-details.html')
    
    def test_category_GET_wrong_slug(self):
        response = self.client.get(reverse('ads:category', args=['wrong-slug']))
        self.assertEqual(response.status_code, 404)


class AdvertisementTest(TestCase):

    @classmethod
    def setUpClass(self):
        self.city1 = City.objects.create(city='Bishkek')
        self.category1 = Category.objects.create(
            title='Category 1',
            parent=None
        )
        self.user1 = CustomUser(email='example@gmail.com')
        self.user1.set_password('StrongPassword123!')
        self.user1.save()

    def login(self):
        self.client.force_login(CustomUser.objects.get(email='example@gmail.com'))

    def _get_ad_data(self):
        data = {
            'description': 'This is test description',
            'price': 1000,
            'currency': str(Advertisement.Currency.SOM),
            'city': self.city1,
            'category': self.category1,
            'phone_number': '+996777991122',
            'hide_phone_number': True,
            'email': 'example@google.com',
            'author': self.user1
        }
        return data

    def _get_images_data(self):
        n = 3
        data = {'form-{{i}}-image': get_test_image() for i in range(n)}
        data = {
            'form-INITIAL_FORMS': '0',
            'form-TOTAL_FORMS': '2',
            'form-MAX_NUM_FORMS': '',
        }
        data['form-INITIAL_FORMS'] = '0'
        data['form-INITIAL_FORMS'] = str(n)
        data['form-MAX_NUM_FORMS'] = ''

        return data

    def test_ad_GET(self):
        adv1 = Advertisement.objects.create(**self._get_ad_data())
        response = self.client.get(reverse('ads:ads-details', kwargs={'pk':adv1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ads-details.html')

    def test_ad_GET_wrong_id(self):
        response = self.client.get(reverse('ads:ads-details', kwargs={'pk':999}))
        self.assertEqual(response.status_code, 404)
    
    def test_ad_POST(self):
        self.login()
        formset_management_data = {
            'images-TOTAL_FORMS': 0, 
            'images-INITIAL_FORMS': 0 
        }
        response = self.client.post(
            reverse('ads:ads-create'),
            data={
                **self._get_ad_data(),
                **formset_management_data,
                'city': self.city1.id,
                'category': self.category1.id,
            },
            follow=True
        )
        last_added = Advertisement.objects.last()

        self.assertRedirects(response, reverse('ads:ads-details', kwargs={'pk': last_added.pk}))
        self.assertEqual(last_added.description, 'This is test description')
        self.assertEqual(last_added.price, 1000)
        self.assertEqual(Advertisement.objects.all().count(), 1)

    def test_ad_POST_no_login_redirects(self):
        response = self.client.get(reverse('ads:ads-create'))
        self.assertRedirects(response, '/account/login/?next=/ads/post/')

    def test_ad_UPDATE_GET_page(self):
        self.login()
        adv1 = Advertisement.objects.create(**self._get_ad_data())
        response = self.client.get(reverse('ads:ads-edit', kwargs={'pk': adv1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ads/ads-edit.html')

    def test_ad_UPDATE_POST(self):
        self.login()
        adv1 = Advertisement.objects.create(**self._get_ad_data())
        formset_management_data = {
            'images-TOTAL_FORMS': 1, 
            'images-INITIAL_FORMS': 0 
        }
        update_data = {
            **self._get_ad_data(),
            **formset_management_data,
            'city': self.city1.id,
            'category': self.category1.id,
            'price': 9999,
            'currency': str(Advertisement.Currency.USD),
            'email': 'xyz@gmail.com',
        }
        response = self.client.post(
            reverse('ads:ads-edit', kwargs={'pk': adv1.id}),
            data=update_data,
            format='multipart'
        )
        adv1.refresh_from_db()
        self.assertEqual(adv1.price, 9999)
        self.assertEqual(adv1.currency, Advertisement.Currency.USD)
        self.assertEqual(adv1.email, 'xyz@gmail.com')

    def test_adv_UPDATE_no_login_redirects(self):
        adv1 = Advertisement.objects.create(**self._get_ad_data())
        response = self.client.get(reverse('ads:ads-edit', kwargs={'pk':adv1.id}))

    @classmethod
    def tearDownClass(self):
        pass