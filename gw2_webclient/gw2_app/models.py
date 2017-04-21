from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

class InstanceMixin(object):
    """Makes sure that no more than nine instance of a given model is created."""

    def clean(self):
        model = self.__class__
        if model.objects.count() > 8:
            raise ValidationError("Can only create 9 %s instance" % model.__name__)
        super(InstanceMixin, self).clean()


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    apikey = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.user.username


class Profession(InstanceMixin, models.Model):
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

    profession_type = models.CharField(max_length=20,unique=True, choices=PROFESSIONS)
    character = models.ForeignKey('Character', on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return self.profession_type


class Character(InstanceMixin, models.Model):
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
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20, null=False)
    race = models.CharField(max_length=10, choices=RACE)
    gender = models.CharField(max_length=10, choices=GENDER)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(80)])
    guild = models.CharField(max_length=50, blank=True)

    def __unicode__(self):
        return self.name


class GameMode(models.Model):
    game_id = models.AutoField(primary_key=True)
    player = models.ManyToManyField(PlayerProfile)


class PveMode(GameMode):
    pve_id = models.AutoField(primary_key=True)


class PveEvent(PveMode):
    event_name = models.CharField(max_length=20, null=True)
    event_boss_name = models.CharField(max_length=20, null=True)
    event_hardcore_boss_name = models.CharField(max_length=20, null=True, blank=True)
    event_time = models.TimeField()

    def __unicode__(self):
        return self.event_name


class PvePersonalStory(PveMode):
    current_story_step_name = models.CharField(max_length=30, null=True)
    current_story_objective = models.CharField(max_length=50, null=True)
    current_story_description = models.TextField(null=True)

    def __unicode__(self):
        return self.current_story_step_name


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


class Achievement(models.Model):
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20, null=True)
    description = models.TextField(null=True)

    def __unicode__(self):
        return self.name


class DailyAchievement(Achievement):
    TYPES = (
        ('PvE', 'Player vs Enviromnent'),
        ('PvP', 'Player vs Player'),
        ('Fractal', 'Fractal'),
    )
    type = models.CharField(max_length=10, choices=TYPES, null=True)

    def __unicode__(self):
        return self.name


class GeneralAchievement(Achievement):
    requirements = models.TextField(null=True)

    def __unicode__(self):
        return self.name
