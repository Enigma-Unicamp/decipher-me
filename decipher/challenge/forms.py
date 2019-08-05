'''
Decipher challenge forms
'''

from django.contrib.auth.password_validation import validate_password
from django import forms

from .models import User, Challenge


class ChallengeForm(forms.ModelForm):

    class Meta:
        model = Challenge
        fields = [
            'flag',
        ]
        help_texts = {
            'flag': 'flag',
        }
        labels = {
            'flag': 'flag',
        }
        widgets = {
            'flag': forms.TextInput(attrs={'placeholder': 'secomp{flag}'})
        }



class LoginForm(forms.Form):

    username_max_length = User._meta.get_field('username').max_length
    password_max_length = User._meta.get_field('password').max_length

    username = forms.CharField(
        label='username',
        max_length=username_max_length,
        help_text='username')
    password = forms.CharField(
        label='password',
        max_length=password_max_length,
        widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def invalidLoginMessage(self):
        self.add_error(
            'username',
            forms.ValidationError("Invalid username or password.")
        )



class RegisterForm(forms.ModelForm):

    password_confirmation = forms.CharField(
        label='password confirmation',
        help_text='confirm your password',
        max_length=User._meta.get_field('password').max_length,
        widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
        ]
        help_texts = {
            'email': 'email',
            'username': 'username',
            'password': 'password',
        }
        labels = {
            'email': 'email',
            'username': 'username',
            'password': 'password',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        # check if password and password confirmation match
        if password != password_confirmation:
            self.add_error(
                'password_confirmation',
                forms.ValidationError("The two password fields didn't match.")
            )

        # password validation (using validators defined in settings.py)
        try:
            validate_password(password)
        except forms.ValidationError as error:
            self.add_error('password_confirmation', error)

        # check if email has not yet been taken
        if User.objects.filter(email=email):
            self.add_error(
                'email',
                forms.ValidationError("This email address is already in use.")
            )

        # check if username has not yet been taken
        if User.objects.filter(username=username):
            self.add_error(
                'username',
                forms.ValidationError("This username is already in use.")
            )

        return cleaned_data



class PasswordChangeForm(forms.Form):

    password_max_length = User._meta.get_field('password').max_length

    new_password = forms.CharField(
        label='new password',
        help_text='inser new password',
        max_length=password_max_length,
        widget=forms.PasswordInput)
    new_password_confirmation = forms.CharField(
        label='new password confirmation',
        help_text='confirm your password',
        max_length=password_max_length,
        widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        new_password_confirmation = cleaned_data.get(
            "new_password_confirmation"
        )

        # check if password and password confirmation match
        if new_password != new_password_confirmation:
            self.add_error(
                'new_password_confirmation',
                forms.ValidationError("The two password fields didn't match.")
            )

        # password validation (using validators defined in settings.py)
        try:
            validate_password(new_password)
        except forms.ValidationError as error:
            self.add_error('new_password_confirmation', error)

        return cleaned_data



# This is SetPasswordForm from django.contrib.auth.forms.
# I got their code but changed max length for password fields.
# I also made a change in the raise error logic.
# https://docs.djangoproject.com/en/1.8/_modules/django/contrib/auth/forms/
class PasswordResetConfirmForm(forms.Form):

    password_max_length = User._meta.get_field('password').max_length

    new_password1 = forms.CharField(
        label='new password',
        help_text='inser new password',
        max_length=password_max_length,
        widget=forms.PasswordInput)
    new_password2 = forms.CharField(
        label='new password confirmation',
        help_text='confirm your password',
        max_length=password_max_length,
        widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordResetConfirmForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:

            # check if password and password confirmation match
            if password1 != password2:
                self.add_error(
                    'new_password2',
                    forms.ValidationError("The two password fields "
                                          + "didn't match.")
                )

            # password validation (using validators defined in settings.py)
            try:
                validate_password(password2)
            except forms.ValidationError as error:
                self.add_error('new_password2', error)

        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()

        return self.user
