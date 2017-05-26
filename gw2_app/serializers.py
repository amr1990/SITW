from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.relations import HyperlinkedIdentityField

from models import Character
from models import Weapon, ProfessionBuild


class WeaponSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(view_name='weapon-detail')

    class Meta:
        model = Weapon
        fields = ('uri', 'name')


class ProfessionSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(view_name='profession-detail')

    class Meta:
        model = ProfessionBuild
        fields = ('uri', 'name')


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    uri = HyperlinkedIdentityField(view_name='character-detail')
    player = CharField(read_only=True)

    class Meta:
        model = Character
        fields = ('uri', 'player', 'name', 'race', 'gender', 'level', 'guild', 'profession_type')
