'''
Decipher challenge forms
'''

from django import forms
from .models import User



class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        help_texts = {
            'username': 'username',
            'password': 'password',
        }
        labels = {
            'username': 'username',
            'password': 'password',
        }
        widgets = {
            'password': forms.PasswordInput(),
        }



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
        if password != confirm_password:
            self.add_error(
                'confirm_password',
                forms.ValidationError("Passwords do not match")
            )
