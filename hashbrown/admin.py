from django.contrib import admin

from .models import Switch
from .utils import ADMIN_FORM_KEY, get_defaults, import_string


class SwitchAdmin(admin.ModelAdmin):
    _custom_forms = {}

    list_display = ('label', 'globally_active', 'description')
    list_editable = ('globally_active',)

    def get_form(self, request, obj=None, **kwargs):
        form_name = get_defaults()[ADMIN_FORM_KEY]

        if not form_name:
            return super(SwitchAdmin, self).get_form(request, obj=obj, **kwargs)

        if form_name not in self._custom_forms:
            form_class = import_string(form_name)
            self._custom_forms[form_name] = form_class

        return self._custom_forms[form_name]


admin.site.register(Switch, SwitchAdmin)
