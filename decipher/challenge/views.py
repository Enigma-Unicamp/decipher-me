'''
Decipher challenge views
'''

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
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

        challs = Challenge.objects.all()
        return render(request, self.template_name, { 'challenges' : challs })



class ChallengeView(LoginRequiredMixin, View):

    template_name = 'challenge/challenge.html'

    def post(self, request, *args, **kwargs):

        chall = get_object_or_404(
            Challenge,
            id_chall=request.POST['id_chall']
            )
        # checa se o usuário tem permissão para ver o desafio em questão
        if request.user.level < chall.id_chall:
            return redirect('challenge:index')
        # se nao tem 'flag' no post, a pessoa so quer ver a pagina do desafio
        if not "flag" in request.POST.keys():
            return render(request, self.template_name, { 'challenge' : chall })

        # se tiver, validamos a flag
        flag = request.POST['flag']
        hash_flag = sha256(bytes(flag, 'utf-8')).hexdigest()

        # objeto para verificar o formato regex da flag
        pattern = re.compile("enigma{+[\x21-\x7E]+}$")

        # flag no formato 'enigma{flag}' e está correta
        if (pattern.match(flag) and hash_flag == chall.flag):
            if request.user.level == chall.id_chall:
                request.user.level += 1
                request.user.last_capture = datetime.now()
                request.user.save()
            return redirect('challenge:home')
        # flag incorreta
        else:
            return render(
                request,
                'challenge/chall_{}.html'.format(chall.id_chall),
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
