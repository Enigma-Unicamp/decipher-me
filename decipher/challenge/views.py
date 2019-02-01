'''
Decipher challenge views
'''
import json
from datetime import datetime
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
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
            challs = Challenge.objects.all().values()

            # concatenate challenge info with field that tells if user has done it
            if not settings.SEQUENTIAL_CHALLENGES:
                challs_done = json.loads(request.user.challenges_done)

                for i in range(len(challs)):
                    challs[i].update({ 'is_done' : challs_done[i] })

            return render(
                request, self.template_name,
                { 'challenges' : challs,
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
                    request.user.last_capture = datetime.now(tz=timezone.utc)
                    request.user.save()

            else:
                challenges_done = json.loads(request.user.challenges_done)
                if challenges_done[chall.id_chall] != '1':
                    challenges_done[chall.id_chall] = '1'
                    request.user.challenges_done = json.dumps(challenges_done)
                    request.user.last_capture = datetime.now(tz=timezone.utc)
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
                last_capture=datetime.now(tz=timezone.utc),
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



class RankingView(LoginRequiredMixin, View):

    template_name = 'challenge/ranking.html'

    def get(self, request, *args, **kwargs):

        ranking = []
        users = User.objects.filter(is_staff=False)

        if settings.SEQUENTIAL_CHALLENGES:
            for user in users:
                # add every user to ranking at position 0
                # after sorting we'll update the positions
                ranking.append({'position' : 0, 'username': user.username, 
                                'points': user.level, 
                                'last_capture': user.last_capture}
                              )

        else:
            chall_points = Challenge.objects.all().values_list('points', flat=True)
            for user in users:
                points = 0

                challenges_done = json.loads(user.challenges_done)
                for i in range(len(challenges_done)):
                    if challenges_done[i] == '1':
                        points += chall_points[i]
                # add every user to ranking at position 0
                # after sorting we'll update the positions
                ranking.append({'position' : 0, 'username': user.username, 
                                'points': points, 
                                'last_capture': user.last_capture}
                              )

        # Sort according to user level and last capture,
        # descending and ascending, respectively.
        ranking.sort(key=lambda item: (-item['points'], item['last_capture']))

        # update each user position in ranking
        for i in range(0, len(ranking)):
            ranking[i]['position'] = i + 1

        return render(request, self.template_name, {'ranking': ranking})



class LogoutView(LoginRequiredMixin, View):

    template_name = 'challenge/ranking.html'

    def get(self, request, *args, **kwargs):

        logout(request)
        return redirect('challenge:index')



class PasswordChangeView(LoginRequiredMixin, TemplateView):

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

            # Get user object
            username = request.user.username
            user = User.objects.get(username__exact=username)

            # Change user password
            new_password = form.cleaned_data.get("new_password")
            user.set_password(new_password)
            user.save()

            # Redirect user to login page with success message
            messages.success(
                request, "Password change successful. "
                + "Please login again."
            )
            return redirect('challenge:login')

        # Otherwise render change password page again
        return render(request, self.template_name, {'form': form})



class PasswordResetCompleteView(TemplateView):

    # Redirect to login page with success message
    def dispatch(self, request, *args, **kwargs):
        messages.success(
            request, "Password reset successful. "
            + "Please login again."
        )
        return redirect('challenge:login')
