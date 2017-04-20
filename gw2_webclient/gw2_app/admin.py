from django.contrib import admin

# Register your models here.
from models import PlayerProfile, Character, Profession, GeneralAchievement, DailyAchievement, PveEvent, \
    PvePersonalStory, StructuredPvpStat, WvwStat

admin.site.register(PlayerProfile)
admin.site.register(Character)
admin.site.register(Profession)
admin.site.register(GeneralAchievement)
admin.site.register(DailyAchievement)
admin.site.register(PveEvent)
admin.site.register(PvePersonalStory)
admin.site.register(StructuredPvpStat)
admin.site.register(WvwStat)


class InstanceAdminMixin(object):
    """Hides the "Add" button when there is already an instance."""

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        return super(InstanceAdminMixin, self).has_add_permission(request)


class ExampleAdmin(InstanceAdminMixin, admin.ModelAdmin):
    model = Character
