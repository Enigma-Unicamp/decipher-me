'''
Decipher challenge views
'''

from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from . import forms
from .models import User, Challenge

from hashlib import sha256
import re


class IndexView(TemplateView):

    # Redirect to the home page
    def dispatch(self, request, *args, **kwargs):
        return redirect('challenge:home')



class HomeView(TemplateView):

    template_name = 'challenge/home.html'

    def get(self, request, *args, **kwargs):

        # if authenticated, pass the challenges to the template
        if request.user.is_authenticated:
            challs = Challenge.objects.all()
            # challs = Challenge.objects.filter(id_chall__lte=request.user.level)
            return render(
                       request, self.template_name,
                       { 'challenges' : challs ,
                         'sequential' : settings.SEQUENTIAL_CHALLENGES }
                   )
        # otherwise, don't
        return render(request, self.template_name)



class ChallengeView(LoginRequiredMixin, View):

    template_name = 'challenge/challenge.html'

    def post(self, request, *args, **kwargs):

        chall = get_object_or_404(
            Challenge,
            id_chall=request.POST['id_chall']
            )

        # user is allowed or not to check the challenge
        if settings.SEQUENTIAL_CHALLENGES and request.user.level < chall.id_chall:
            return redirect('challenge:index')

        # if the post request has no 'flag', render the challenge page
        if not "flag" in request.POST.keys():

            # 'link type challenge', so open the link file to
            # pass the link to template
            if chall.type_chall == 'link':
                file_path = "challenge/static/" + chall.file_content
                file_object = open(file_path, 'r')
                link = file_object.read()
                return render(
                          request, self.template_name,
                          {'link' : link, 'challenge' : chall }
                          )

            # other types of challenges
            return render(request, self.template_name, { 'challenge' : chall })

        # if it has the 'flag', check if it's correct
        flag = request.POST['flag']
        hash_flag = sha256(bytes(flag, 'utf-8')).hexdigest()

        # pattern to verify regex
        pattern = re.compile("decipher{+[\x21-\x7E]+}$")

        # flag is correct
        if pattern.match(flag) and hash_flag == chall.flag:

            if settings.SEQUENTIAL_CHALLENGES:
                if request.user.level == chall.id_chall:
                    request.user.level += 1
            else:
                if not str(chall.id_chall) in request.user.challenges_done:
                    request.user.challenges_done += str(chall.id_chall)
            request.user.last_capture = datetime.now()
            request.user.save()
            return redirect('challenge:home')

        # flag is incorret
        else:
            return render(
                request, self.template_name,
                {'wrong_flag' : True, 'challenge': chall}
                )



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
            messages.success(request, 'Registration successful.')
            User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                email=form.cleaned_data['email'],
            )
            # Redirect new user to login page
            return redirect('challenge:login')

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
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            # If valid user, redirect to index page
            if user is not None:
                login(request, user)
                return redirect('challenge:index')
            # Otherwise spawn invalid login message
            else:
                form.invalidLoginMessage()

        # Show the login page again (with invalid login message)
        return render(request, self.template_name, {'form': form})



class LogoutView(LoginRequiredMixin, View):

    # Logout user and redirect him to index
    def get(self, request, *args, **kwargs):

        logout(request)
        return redirect('challenge:index')



class PasswordChangeView(TemplateView):

    template_name = 'challenge/password_change.html'
    form_class = forms.PasswordChangeForm

    # Render change password form
    def get(self, request, *args, **kwargs):

        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    # Handle password change attempt
    def post(self, request):

        form = self.form_class(request.POST)

        # If the form is valid change user password
        if form.is_valid():
            messages.success(
                request, "Password change successful. "
                + "Please login again."
            )

            # Get user object
            username = request.user.username
            user = User.objects.get(username__exact=username)
        
            # Change user password
            new_password = form.cleaned_data.get("new_password")

            print(username)
            print(new_password)
            user.set_password(new_password)
            user.save()

            # Redirect user to login page
            return redirect('challenge:login')

        # Otherwise render change password page again
        return render(request, self.template_name, {'form': form})
