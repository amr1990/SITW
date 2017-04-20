from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.


class PlayerProfile(models.Model):
    user = models.OneToOneField(User)
    apikey = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user.username


class Profession(models.Model):
    PROFESSIONS = (
        ('Guardian', 'Guardian'),
        ('Mesmer', 'Mesmer'),
        ('Warrior', 'Warrior'),
        ('Necromancer', 'Necromancer'),
        ('Revenant', 'Revenant'),
        ('Ranger', 'Ranger'),
        ('Engineer', 'Engineer'),
        ('Elementalist', 'Elementalist'),
        ('Thief', 'Thief'),
    )

    profession_type = models.CharField(max_length=20, choices=PROFESSIONS)

    def __unicode__(self):
        return self.profession_type



class Character(models.Model):
    RACE = (
        ('Norn', 'Norn'),
        ('Asura', 'Asura'),
        ('Sylvary', 'Sylvary'),
        ('Charr', 'Charr'),
        ('Human', 'Human'),
    )
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    name = models.CharField(max_length=20, null=False)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE)
    race = models.CharField(max_length=10, choices=RACE)
    gender = models.CharField(max_length=10, choices=GENDER)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(80)])
    guild = models.CharField(max_length=50, blank=True)


class GameMode(models.Model):
    game_id = models.AutoField(primary_key=True)
    player = models.ManyToManyField(PlayerProfile)

    def __unicode__(self):
        return self.game_id

class PvpMode(GameMode):
    pvp_id = models.AutoField(primary_key=True)


class StructuredPvpStat(PvpMode):
    ranking = models.IntegerField(null=True)
    win_lose_ratio = models.IntegerField(null=True)
    league = models.CharField(max_length=20, null=True)

    def __unicode__(self):
        return self.league


class WvwStat(PvpMode):
    objective_name = models.CharField(max_length=20, null=True)
    objective_sector = models.CharField(max_length=20, null=True)
    objective_map = models.CharField(max_length=20, null=True)
    time_start = models.TimeField(null=True)
    time_end = models.TimeField(null=True)

    def __unicode__(self):
        return self.objective_name