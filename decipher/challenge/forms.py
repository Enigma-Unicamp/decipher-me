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
        pass_min_length = 6
        if password != confirm_password:
            self.add_error(
                'confirm_password',
                forms.ValidationError("Passwords do not match.")
            )
        elif len(password) < pass_min_length:
            self.add_error(
                'password',
                forms.ValidationError("Your password must have at least " +
                                      "%d characters." %  pass_min_length)
            )
