from rest_framework.relations import HyperlinkedIdentityField
from rest_framework import serializers
from models import Character
from rest_framework.fields import CharField


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    uri = HyperlinkedIdentityField(view_name='character-detail')
    player = CharField(read_only=True)

    class Meta:
        model = Character
        fields = ('uri', 'player', 'name', 'race', 'gender', 'level', 'guild', 'profession_type')
