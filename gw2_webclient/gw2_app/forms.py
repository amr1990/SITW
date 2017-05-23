from django.contrib.auth.models import User
from django import forms

from models import PlayerProfile, Character


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class PlayerForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = ('apikey',)

class CreateCharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ('name','race','gender','level','guild', 'profession_type')

class EditCharacterForm(forms.ModelForm):
        class Meta:
            model = Character
            fields = ('name', 'race', 'gender', 'level', 'guild', 'profession_type')


