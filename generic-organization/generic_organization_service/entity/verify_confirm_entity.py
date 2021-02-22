from generic_organization_service.models import UserConnection
from generic_organization_service.models import VerifyConfirm

from django.core.exceptions import ObjectDoesNotExist
from enum import Enum
import datetime


class VerifyStatus(Enum):
    ABORTED = 'ABORTED'
    SSI_VERIFIED = 'SSI_VERIFIED' #SSI VERIFICATION SUCCESSFULL
    SSI_FAILED = 'SSI_FAILED'  #SSI VERIFICATION FAIL
    COMPLETED = 'COMPLETED' #SSI VERIFICATION AND ORGANIZATION COMPLETE SUCCESSFULLY
    FAILED = 'FAILED'  #ORGANIZATION VERIFICATION FAIL


def create_verify_confirm(verify_request, confirm_date: datetime, verify_status: VerifyStatus, proof_evidence,
                          proof_request, user_connection: UserConnection):
    request = VerifyConfirm.objects.create(verify_request=verify_request, confirm_date=confirm_date,
                                           status=verify_status.value, proof_evidence=proof_evidence,
                                           proof_request=proof_request, user_connection=user_connection)
    return request


def update_verify_confirm(verify_confirm:VerifyConfirm, status:VerifyStatus):
    verify_confirm.status = status.value
    verify_confirm.save()
    return verify_confirm

def get_verify_confirm(id=None, confirm_date=None, verify_status=None, user=None, user_business_uid=None) -> VerifyConfirm:
    try:
        filters = dict()
        if confirm_date:
            filters['confirm_date'] = confirm_date
        if id:
            filters['id'] = id
        if verify_status:
            filters['verify_status'] = verify_status
        if user:
            filters['user'] = user
        if user_business_uid:
            filters['user__business_uid'] = user_business_uid

        confirm = VerifyConfirm.objects.get(**filters)
    except ObjectDoesNotExist:
        confirm = None
    return confirm


def list_verify_confirm(id=None, confirm_date=None, verify_status=None, user=None, user_business_uid=None):
    try:
        filters = dict()
        if confirm_date:
            filters['confirm_date'] = confirm_date
        if id:
            filters['id'] = id
        if verify_status:
            filters['verify_status'] = verify_status
        if user:
            filters['user'] = user
        if user_business_uid:
            filters['user__business_uid'] = user_business_uid

        confirm = VerifyConfirm.objects.filter(**filters)
    except ObjectDoesNotExist:
        confirm = None
    return confirm
