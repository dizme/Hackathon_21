from generic_organization_service.models import Credential
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


def create_credential(name: str, business_code: str, version: str, attributes: str):
    credential = Credential.objects.create(name=name, business_code=business_code, version=version,
                                           attributes=attributes)
    return credential


def find_credentials(name, business_code, version):
    try:
        filters = dict()

        if name:
            filters['name'] = name
        if business_code:
            filters['business_code'] = business_code
        if version:
            filters['version'] = version

        credential = Credential.objects.filter(**filters)
    except ObjectDoesNotExist:
        return None
    return credential


def find_credential(name, business_code=None, version=None) -> Credential:
    try:
        filters = dict()

        if name:
            filters['name'] = name
        if business_code:
            filters['business_code'] = business_code
        if version:
            filters['version'] = version

        credential = Credential.objects.get(**filters)
    except ObjectDoesNotExist:
        return None
    return credential


def get_credential_by_business_code(business_code: str) -> Credential:
    logger.debug("Credential business code: %s ", business_code)
    try:
        filters = dict()
        filters['business_code'] = business_code
        credential = Credential.objects.get(**filters)
    except ObjectDoesNotExist:
        return None
    return credential

