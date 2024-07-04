from django.urls import reverse, resolve
from django.test import SimpleTestCase
from home.views import Home, About


class TestUrls(SimpleTestCase):
    def test_home(self):
        url = reverse('home:home') # take the url name and its args and bring back the path 
        # the resilve(url).func.view_class for telling that the url view is a class view
        self.assertEqual(resolve(url).func.view_class, Home) # resolve is a method that bring back some ingo about a url name like it connect to wich view

    def test_about(self):
        url = reverse('home:about', args=['nima']) # /about/nima
        self.assertEqual(resolve(url).func.view_class, About)
        