from generic_organization_service.models import Properties
from django.core.exceptions import ObjectDoesNotExist


def add_property(name, value):
    prop = Properties.objects.create(name=name, value=value)
    return prop


def get_property_by_name(name):
    prop = None
    try:
        props = Properties.objects.filter(name=name)
        prop = props[0]
        return prop.value
    except ObjectDoesNotExist:
        return None


def get_properties():
    prop = Properties.objects.all()
    return prop
