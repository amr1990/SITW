from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.relations import HyperlinkedIdentityField

from models import Character, Trait, Specialization
from models import Weapon, ProfessionBuild, WeaponSkill


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


class WeaponSkillSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(view_name='weaponskill-detail')
    weapon = WeaponSerializer(read_only=True)

    class Meta:
        model = WeaponSkill
        fields = ('uri', 'name', 'description', 'weapon')


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    uri = HyperlinkedIdentityField(view_name='character-detail')
    player = CharField(read_only=True)

    class Meta:
        model = Character
        fields = ('uri', 'player', 'name', 'race', 'gender', 'level', 'guild', 'profession_type')


class TraitSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(view_name='trait-detail')

    class Meta:
        model = Trait
        fields = ('uri', 'name', 'description', 'ismajor')


class SpecSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(view_name='spec-detail')

    class Meta:
        model = Specialization
        fields = ('uri', 'name', 'iselite')
