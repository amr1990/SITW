from django.contrib import admin

# Register your models here.
from models import UserProfile, Character, Profession

admin.site.register(UserProfile)
admin.site.register(Character)
admin.site.register(Profession)