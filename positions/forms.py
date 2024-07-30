from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    api_key = forms.CharField(widget=forms.PasswordInput, required=True)
    api_secret = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'api_key', 'api_secret')

class UpdateTokenForm(forms.Form):
    api_key = forms.CharField(widget=forms.PasswordInput, required=True)
    api_secret = forms.CharField(widget=forms.PasswordInput, required=True)
