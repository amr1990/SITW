from django.contrib.auth.models import User
from django import forms

from models import PlayerProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class PlayerForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = ('apikey',)
