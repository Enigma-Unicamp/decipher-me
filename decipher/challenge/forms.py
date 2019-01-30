'''
Decipher challenge forms
'''

from django import forms
from .models import User


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

    def invalidLoginMessage(self):
        self.add_error(
            'username',
            forms.ValidationError("Invalid username or password.")
        )



class RegisterForm(forms.ModelForm):

    confirm_password=forms.CharField(
        label='confirm password',
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
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        # check if password size is ok
        pass_min_length = 6
        if password != confirm_password:
            self.add_error(
                'confirm_password',
                forms.ValidationError("Passwords do not match.")
            )

        # try to match password and confirm password
        elif len(password) < pass_min_length:
            self.add_error(
                'password',
                forms.ValidationError("Your password must have at least " +
                                      "%d characters." %  pass_min_length)
            )

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
                forms.ValidationError("Your username must have at least " +
                                      "%d characters." %  user_min_length)
            )
