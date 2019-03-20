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



class ChallengesPageView(LoginRequiredMixin, View):

    template_name = 'challenge/challenges_page.html'

    def get(self, request, *args, **kwargs):

        # if authenticated, pass the challenges to the template
        if request.user.is_authenticated:
            challs = list(Challenge.objects.all().values())

            # concatenate challenge info with field that
            # says if user has unlocked or not the challenge
            # and info that says if user has done ir ot not
            challenges_done = json.loads(request.user.challenges_done)

            # total number of users
            n_users = len(User.objects.all())

            # if there's at least one user, compute percentage
            if n_users > 0:
                for i in range(0, len(challs)):
                    # print(challs[i]['solved_by'])
                    challs[i]['solved_by'] = challs[i]['solved_by'] / n_users
                    # print(challs[i]['solved_by'])
                    challs[i]['solved_by'] *= 100
                    # print(challs[i]['solved_by'])
                    # print()
            # if there's no user, just set it to zero
            else:
                for i in range(0, len(challs)):
                    challs[i]['solved_by'] = 0

            if settings.SEQUENTIAL_CHALLENGES:

                # for sequential challenges, challenge 0 may be done or
                # not, but is always unlocked for everybody
                challs[0]['is_done'] = challenges_done[0]
                challs[0]['locked'] = '0'

                # from challenge 1 onwards, we need to verify if
                # it's unlocked or not
                for i in range(1, len(challs)):
                    if challenges_done[i] == '1':
                        is_done = '1'
                        locked = '0'
                    elif challenges_done[i - 1] == '1':
                        is_done = '0'
                        locked = '0'
                    else:
                        is_done = '0'
                        locked = '1'
                    challs[i]['is_done'] = is_done
                    challs[i]['locked'] = locked

            # for non sequential challenges, every challenge is unlocked 
            else:
                for i in range(0, len(challs)):
                    is_done = challenges_done[i]
                    locked = '0'
                    challs[i]['is_done'] = is_done
                    challs[i]['locked'] = locked

            return render(
                request, self.template_name,
                { 'challenges' : challs,
                  'sequential' : settings.SEQUENTIAL_CHALLENGES }
            )

        # otherwise, don't
        return render(request, self.template_name)



class ChallengeView(LoginRequiredMixin, View):

    template_name = 'challenge/challenge.html'
    form_class = forms.ChallengeForm

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST)

        chall = get_object_or_404(
                  Challenge,
                  id_chall=request.POST['id_chall']
                )

        # challenges done by user
        challenges_done = json.loads(request.user.challenges_done)

        # user isn't allowed to check this challenge
        if settings.SEQUENTIAL_CHALLENGES:
            if chall.id_chall != 0:
                if challenges_done[chall.id_chall - 1] == '0':
                    return redirect('challenge:index')

        # 'link type challenge', so open the link file to
        # pass the link to template
        if chall.type_chall == 'link':
            file_path = "challenge/static/" + chall.file_content
            file_object = open(file_path, 'r')
            link = file_object.read()
        else:
            link = None

        # we're gonna use this to show specific errors to users
        flag_resubmission = False
        wrong_flag = False

        # check if it's a flag submission 
        if "flag" in request.POST.keys():

            # guarantee that's not a resubmission
            if challenges_done[chall.id_chall] == '0':

                # now let's check if the flag is correct
                flag = request.POST['flag']
                hash_flag = sha256(bytes(flag, 'utf-8')).hexdigest()

                # pattern to verify regex
                pattern = re.compile("decipher{+[\x21-\x7E]+}$")

                # flag is correct
                if pattern.match(flag) and hash_flag == chall.flag:

                    challenges_done[chall.id_chall] = '1'
                    request.user.challenges_done = json.dumps(challenges_done)
                    request.user.points += chall.points
                    request.user.last_capture = datetime.now(tz=timezone.utc)
                    print(chall.solved_by)
                    chall.solved_by += 1
                    print(chall.solved_by)
                    request.user.save()
                    chall.save()

                    return redirect('challenge:challenges_page')

                # otherwise the flag is incorrect
                else:
                    wrong_flag = True

            # it's a resubmission
            else:
                flag_resubmission = True

        # select the 'correct error' to show
        error_message = None
        if flag_resubmission:
            error_message = "You have already completed this challenge."
        elif wrong_flag:
            error_message = "Wrong flag :("

        # total number of users
        n_users = len(User.objects.all())

        # percentage of users that solved this challenge
        if n_users > 0:
            chall.solved_by = chall.solved_by / n_users
            chall.solved_by *= 100
        # if there's no user, just set it to zero
        else:
            chall.solved_by = 0

        # render the challenge page
        return render(
            request, self.template_name,
            { 'error_message' : error_message, 'link' : link, 
              'challenge': chall, 'form' : form }
        )



class RulesView(LoginRequiredMixin, TemplateView):

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
                email=form.cleaned_data['email'],
                points=0,
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
        ranking = users.order_by('-points', 'last_capture')

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
