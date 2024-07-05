from django.test import TestCase, Client
from home.forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.urls import reverse


class TestUserRegistrationView(TestCase):
    
    def setUp(self):
        self.client = Client()
    # test the get method 
    def test_user_registration_get(self):
        response = self.client.get(reverse('home:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/register.html')
        self.assertEqual(response.context["form"].__class__, UserRegistrationForm)
    
    def test_user_registration_post_valid(self):
        response = self.client.post(reverse('home:register'),data= {
            'username': 'kevin',
            'email':'emai@gmail.com',
            'password1':'123',
            'password2':'123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home:home"))
        self.assertEqual(User.objects.count(), 1)
    
    def test_user_registration_post_invalid(self):
        response = self.client.post(reverse('home:register'),data= {
            'username': 'kevin',
            'email':'emai.com',
            'password1':'123',
            'password2':'123'
        })
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFalse(form.is_valid())
        self.assertFormError(form=form, field='email', errors=['Enter a valid email address.'])
        
class TestWriterView(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username='root', password='root', email='root@email.com')
        self.client = Client()
        self.client.login(username='root', password='root', email='root@email.com')
    
    def test_writers(self):
        response = self.client.get(reverse('home:writers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/writers.html')