from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from models import Weapon, ProfessionBuild, WeaponSkill


class WeaponSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(view_name='weapon-detail')

    class Meta:
        model = Weapon
        fields = ('uri', 'name')


class ProfessionSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(view_name='profession-detail')
    weapons = WeaponSerializer(read_only=True, many=True)

    class Meta:
        model = ProfessionBuild
        fields = ('uri', 'name', 'weapons')


class WeaponSkillSerializer(serializers.ModelSerializer):
    uri = HyperlinkedIdentityField(view_name='weaponskill-detail')
    weapon = WeaponSerializer(read_only=True)
    profession = ProfessionSerializer(read_only=True)

    class Meta:
        model = WeaponSkill
        fields = ('uri', 'name', 'description', 'weapon', 'profession')
