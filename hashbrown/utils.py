import sys
from importlib import import_module

from django.conf import settings
from django.utils import six

from .models import Switch


SWITCH_DEFAULTS_KEY = 'HASHBROWN_SWITCH_DEFAULTS'
ADMIN_FORM_KEY = 'HASHBROWN_ADMIN_FORM'


def is_active(label, user=None):
    defaults = get_defaults()[SWITCH_DEFAULTS_KEY]

    globally_active = defaults[label].get(
        'globally_active',
        False) if label in defaults else False

    description = defaults[label].get(
        'description',
        '') if label in defaults else ''

    switch, created = Switch.objects.get_or_create(
        label=label, defaults={
            'globally_active': globally_active,
            'description': description,
        })

    if created:
        return switch.globally_active

    if switch.globally_active or (
        user and user.available_switches.filter(pk=switch.pk).exists()
    ):
        return True
    return False


def get_defaults():
    return {
        SWITCH_DEFAULTS_KEY: getattr(settings, SWITCH_DEFAULTS_KEY, {}),
        ADMIN_FORM_KEY: getattr(settings, ADMIN_FORM_KEY, ''),
    }


# From Django 1.7.
def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            dotted_path, class_name)
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])
