'''
Decipher challenge forms
'''

from django import forms
from .models import User
from django.contrib.auth.password_validation import validate_password


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
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        return cleaned_data

    def invalidLoginMessage(self):
        self.add_error(
            'username',
            forms.ValidationError("Invalid username or password.")
        )



class PasswordChangeForm(forms.Form):

    password_max_length = User._meta.get_field('password').max_length

    new_password = forms.CharField(
        label='new password',
        help_text='inser new password',
        max_length=password_max_length,
        widget=forms.PasswordInput)
    new_password_confirmation=forms.CharField(
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



class RegisterForm(forms.ModelForm):

    password_confirmation=forms.CharField(
        label='password confirmation',
        help_text='confirm your password',
        max_length=User._meta.get_field('password').max_length,
        widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password',
        ]
        help_texts = {
            'first_name': 'first name',
            'last_name': 'last name',
            'email': 'email',
            'username': 'username',
            'password': 'password',
        }
        labels = {
            'first_name': 'first name',
            'last_name': 'last name',
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

        # check if username size is ok
        user_min_length = 6
        if len(username) < user_min_length:
            self.add_error(
                'username',
                forms.ValidationError("This username is too short. It must " +
                                      "contain at least %d characters." 
                                      %  user_min_length)
            )

        return cleaned_data
