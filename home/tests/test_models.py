from django.db import models
from home.models import Writer
from django.test import TestCase
from model_bakery import baker
class TestrWriterModel(TestCase):
    # setup method will run before all the method 
    def setUp(self):
        # we use model bakery package for creating the fields that we dont have the time to do them now we need f,l name but the email and country is not important
        self.writer = baker.make(
            Writer,
            first_name="kevin",
            last_name="wong",
        )
        
        
    def test_model_str(self):
        
        self.assertEqual(str(self.writer), "kevin wong")
