from generic_organization_service.models import Organization
from django.core.exceptions import ObjectDoesNotExist


def get_organization_by_id(org_id):
    try:
        organization = Organization.objects.get(id=org_id)
    except ObjectDoesNotExist:
        organization = None
    return organization


def get_organization_by_name(name):
    try:
        organization = Organization.objects.get(name=name)
    except ObjectDoesNotExist:
        organization = None
    return organization


def get_organization_by_business_code(business_code):
    try:
        organization = Organization.objects.get(business_code=business_code)
    except ObjectDoesNotExist:
        organization = None
    return organization

