from rest_framework.relations import HyperlinkedIdentityField
from rest_framework import serializers
from models import Character
from rest_framework.fields import CharField


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    uri = HyperlinkedIdentityField(view_name='gw2_app:character-detail')
    player = CharField(read_only=True)

    def create(self, validated_data):
        character = Character(**validated_data)
        character.player = self.request.user.playerprofile
        return character

    class Meta:
        model = Character
        fields = ('uri', 'player', 'name', 'race', 'gender', 'level', 'guild', 'profession_type')
