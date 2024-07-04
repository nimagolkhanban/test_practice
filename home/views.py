from django.shortcuts import render
from django.views import View
# Create your views here.

class Home(View):
    def get(self, request):
        return render(request, 'home/home.html')
    

class About(View):
    def get(self, request, username):
        return render(request, 'home/about.html')