from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from home.forms import UserRegistrationForm
# Create your views here.

class Home(View):
    def get(self, request):
        return render(request, 'home/home.html')
    

class About(View):
    def get(self, request, username):
        return render(request, 'home/about.html')
    
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = "home/register.html"
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(username=cd["username"], password=cd["password1"], email=cd["email"])
            messages.success(request, "User created successfully", "success")
            return redirect("home:home")
        return render(request, self.template_name, {"form": form})