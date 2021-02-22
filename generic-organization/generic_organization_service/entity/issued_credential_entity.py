from generic_organization_service.models import IssuedCredential, IssueRequest, Credential, UserConnection, Organization
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


def create_issued_credential(request:IssueRequest, user_connection: UserConnection, credential: Credential):
    issued_credential = IssuedCredential.objects.create(request_uid=request, credential=credential,
                                                        user_connection=user_connection)
    return issued_credential


def get_issued_credential_by_request_id(request_id) -> IssuedCredential:
    try:
        issued_credential = IssuedCredential.objects.get(request_id=request_id)
    except ObjectDoesNotExist:
        issued_credential = None
    return issued_credential


def issued_credential_by_user(user_connection: UserConnection):
    try:
        issued_credentials = IssuedCredential.objects.filter(user_connection=user_connection)
    except ObjectDoesNotExist:
        issued_credentials = None
    return issued_credentials


def issued_credentials_by_organization(organization: Organization):
    try:
        issued_credentials = IssuedCredential.objects.filter(user_connection__organization=organization)
    except ObjectDoesNotExist:
        issued_credentials = None
    return issued_credentials
