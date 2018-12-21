'''
Decipher challenge views
'''

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from .models import User


class IndexView(TemplateView):

    # Redirect to the home page
    def dispatch(self, request, *args, **kwargs):
        return redirect('challenge:home')


class HomeView(TemplateView):

    template_name = 'challenge/home.html'


class RulesView(TemplateView):

    template_name = 'challenge/rules.html'


class RegisterView(TemplateView):

    template_name = 'challenge/register.html'
    form_class = forms.RegisterForm

    # Render register page
    def get(self, request, *args, **kwargs):

        # Redirect to index if user is already logged in
        if request.user.is_authenticated:
            return redirect()

        # Otherwise show form to register
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # Deal with register request
    def post(self, request):
    
        form = self.form_class(request.POST)

        # If the form is valid create new user object
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                email=form.cleaned_data['email'],
                university=form.cleaned_data['university'],
            )
            # Redirect new user to login page
            #return redirect('d2018:login')
            return

        # Otherwise render register page again
        return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):

    template_name = 'challenge/login.html'
    form_class = forms.LoginForm

    # Render login page
    def get(self, request, *args, **kwargs):
    
        # If the user is already logged redirect him to index
        if request.user.is_authenticated:
            return redirect('challenge:index')

        # Otherwise show him the forms
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # Handle login attempt
    def post(self, request):

        form = self.form_class(request.POST)

        # Check if the attempt is valid
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            # Authenticate user if he's valid
            if user is not None:
                login(request, user)
                print("User {} logged".format(user))
                return redirect('challenge:index')

        # Otherwise show the login page again
        return redirect('challenge:login')


class LogoutView(LoginRequiredMixin, View):

    # Logout user and redirect him to index
    def get(self, request, *args, **kwargs):

        logout(request)
        return redirect('challenge:index')
