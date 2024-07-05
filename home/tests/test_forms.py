from django.test import TestCase
from home.forms import UserRegistrationForm
from django.contrib.auth.models import User


class TestRegistrationForm(TestCase):
    def test_valid_data(self):
        form = UserRegistrationForm(data={'username':'jack', 'email':"jack@gmail.com", 'password1':"jack@123", 'password2':"jack@123"})
        self.assertTrue(form.is_valid())
        
    def test_empty_data(self):
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4) # we have 4 field so lenght of error should be 4
    
    def test_exist_email(self):
        User.objects.create_user(username="kevin", password="kevin@123", email="kevin@gmail.com")
        form = UserRegistrationForm(data={'username':'notkevin', 'email':"kevin@gmail.com", 'password1':"kevin@123", 'password2':"kevin@123"})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error('email')) # we raise a validation error in the email field so we tring to get that
    
    def test_unmatched_password(self):
        form = UserRegistrationForm(data={'username':'mark', 'email':"mark@gmail.com", 'password1':"kevin@123", 'password2':"kevin@12"})
        self.assertEqual(len(form.errors), 1)
        self.assertTrue(form.has_error)
        
        
        
