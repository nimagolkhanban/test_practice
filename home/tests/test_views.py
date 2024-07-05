from django.test import TestCase, Client, RequestFactory
from home.forms import UserRegistrationForm
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from home.views import Home

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
        
class test_home_view(TestCase):
    def setUp(self):
         self.user = User.objects.create_user(username='root', password='root', email='root@email.com')
         self.factory = RequestFactory()
         
    # in this section we need to check if the user is loged in or annonymous user so we need to have access to the request rather than response
    # so we use request factory for cloning the request and add the user to request the way we want 
    def test_home_user_authenticated(self):
        request = self.factory.get(reverse('home:home'))
        request.user = self.user
        # the syntax is for view class , we pass the request like this 
        response = Home.as_view()(request)
        self.assertEqual(response.status_code, 302)
        
    def test_home_user_annonymous(self):
        request = self.factory.get(reverse('home:home'))
        request.user = AnonymousUser()
        response = Home.as_view()(request)
        self.assertEqual(response.status_code, 200)