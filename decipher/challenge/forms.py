'''
Decipher challenge forms
'''

from django import forms
from .models import User


class LoginForm(forms.Form):

    username = forms.CharField(
        label='username',
        max_length=50,
        help_text='username')
    password = forms.CharField(
        label='password',
        max_length=20,
        widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    '''
    Formulário de Cadastro dos usuários
    @model: baseado no modelo de usuário
    @fields: campos que serão usados
    @labels: labels
    @helptext: texto de ajuda
    '''
    confirm_password=forms.CharField(
        label='confirme a senha',
        help_text='confirme a senha',
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
            'first_name': 'primeiro nome',
            'last_name': 'sobrenome',
            'email': 'e-mail',
            'username': 'usuário',
            'password': 'senha',
        }
        labels = {
            'first_name': 'primeiro nome',
            'last_name': 'sobrenome',
            'email': 'e-mail',
            'username': 'usuário',
            'password': 'senha',
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
