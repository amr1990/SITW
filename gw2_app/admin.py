from django.contrib import admin

# Register your models here.
from models import *

admin.site.register(ProfessionBuild)
admin.site.register(Weapon)
admin.site.register(WeaponSkill)
admin.site.register(Trait)
admin.site.register(ProfessionSkill)
admin.site.register(Specialization)
admin.site.register(Profile)
admin.site.register(WeaponSet)
admin.site.register(Build)
admin.site.register(Character)


class InstanceAdminMixin(object):
    """Hides the "Add" button when there is already an instance."""

    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        return super(InstanceAdminMixin, self).has_add_permission(request)


class ExampleAdmin(InstanceAdminMixin, admin.ModelAdmin):
    model = Character
