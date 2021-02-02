from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms


User = get_user_model()


class CustomUserTest(TestCase):
    def setUp(self):
        self.email = 'example@gmail.com'
        self.phone = '+996999123456'
        self.password = 'A123456789bc!'

    def test_user(self):
        user = User(email=self.email, password=self.password)
        user.full_clean()

    def test_signup_page(self):
        response = self.client.get(reverse('custom_user:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup_form_with_email(self):
        response = self.client.post(reverse('custom_user:signup'), data={
            'email': self.email,
            'password1': self.password,
            'password2': self.password
        })
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(response.status_code, 302)
    
    def test_signup_form_with_phone_number(self):
        response = self.client.post(reverse('custom_user:signup'), data={
            'phone_number': self.phone,
            'password1': self.password,
            'password2': self.password
        })
        users = User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(response.status_code, 302)
    
    def test_signup_form_without_email_and_phone_number(self):
        response = self.client.post(reverse('custom_user:signup'), data={
            'password1': self.password,
            'password2': self.password
        })
        users = User.objects.all()
        self.assertEqual(users.count(), 0)
        self.assertRaisesMessage(forms.ValidationError, 'Either email or phone number must be set')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse('custom_user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/login.html')

    def test_login_form_with_email(self):
        user = User(email=self.email, password=self.password)
        user.set_password(self.password)
        user.save()
        users = User.objects.all()
        response = self.client.post(reverse('custom_user:login'), data={
            'username': self.email,
            'password': self.password
        }, follow=True)
        self.assertEqual(users.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_form_with_phone(self):
        user = User(phone_number=self.phone, password=self.password)
        user.set_password(self.password)
        user.save()
        users = User.objects.all()
        response = self.client.post(reverse('custom_user:login'), data={
            'username': self.phone,
            'password': self.password
        }, follow=True)
        self.assertEqual(users.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
    
    
    def test_login_form_with_email_wrong(self):
        user = User(email=self.email, password=self.password)
        user.set_password(self.password)
        user.save()
        users = User.objects.all()
        response = self.client.post(reverse('custom_user:login'), data={
            'username': 'wrong@email.com',
            'password': self.password
        }, follow=True)
        self.assertEqual(users.count(), 1)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)