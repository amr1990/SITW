from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
from django.urls import reverse


class InstanceMixin(object):
    """Makes sure that no more than nine instance of a given model is created."""

    def clean(self):
        model = self.__class__
        if model.objects.count() > 8:
            raise ValidationError("Can only create 9 %s instance" % model.__name__)
        super(InstanceMixin, self).clean()


class Profile(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100,null=True)
    user = models.OneToOneField(User, unique=True,related_name='profile')
    apikey = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.user.username


class ProfessionBuild(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False)
    weapons = models.ManyToManyField('Weapon')

    def __unicode__(self):
        return str(self.name)


class Weapon(models.Model):
    name = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return str(self.name)


class Build(models.Model):
    name = models.CharField(max_length=100, null=True, blank=False)
    profession = models.ForeignKey('ProfessionBuild', on_delete=models.CASCADE, null=True)
    weaponset = models.ManyToManyField('WeaponSet')
    character = models.ForeignKey('Character', on_delete=models.CASCADE, null=True)

    def __unicode__(self):
        return str(self.name)


class WeaponSet(models.Model):
    weapon1 = models.ManyToManyField('Weapon')

    def __unicode__(self):
        a = "Weaponset: "
        for b in self.weapon1.all():
            a = a + str(b.name) + ", "
        return str(a)


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

    player = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20, null=False)
    race = models.CharField(max_length=10, choices=RACE)
    gender = models.CharField(max_length=10, choices=GENDER)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(80)])
    guild = models.CharField(max_length=50, blank=True)
    PROFESSIONS = (
        ('Thief', 'Thief'),
        ('Guardian', 'Guardian'),
        ('Mesmer', 'Mesmer'),
        ('Warrior', 'Warrior'),
        ('Necromancer', 'Necromancer'),
        ('Revenant', 'Revenant'),
        ('Ranger', 'Ranger'),
        ('Engineer', 'Engineer'),
        ('Elementalist', 'Elementalist'),
    )

    profession_type = models.CharField(max_length=20, null=True, choices=PROFESSIONS)

    def get_absolute_url(self):
        return reverse('edit_char', kwargs={'char_id': self.id})

    def __unicode__(self):
        return self.name
