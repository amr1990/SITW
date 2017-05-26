from django.contrib.auth.models import User
from django import forms

from models import Character, Profile, Build, WeaponSet


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('city', 'country', 'apikey')


class CreateCharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'race', 'gender', 'level', 'guild', 'profession_type')


class BuildForm(forms.ModelForm):
    class Meta:
        model = Build
        fields = ('name', 'profession', 'weaponset', 'character')


class WeaponSetForm(forms.ModelForm):
    class Meta:
        model = WeaponSet
        fields = ('weapon1',)



