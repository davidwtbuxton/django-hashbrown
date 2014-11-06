from django.contrib import admin
from django.utils.encoding import force_text

from .models import Switch


class SwitchAdmin(admin.ModelAdmin):
    list_display = ('label', 'globally_active', 'active_for_users', 'description')
    list_editable = ('globally_active',)

    def active_for_users(self, obj):
        return u', '.join(force_text(user) for user in obj.users.all())


admin.site.register(Switch, SwitchAdmin)
