from generic_organization_service.models import IqpRequest, IqpDossier, UserConnection
from generic_organization_service.utils.util import datetime_now
from enum import Enum
from django.core.exceptions import ObjectDoesNotExist
import datetime


class RequestStatus(Enum):
    SCHEDULED = 'SCHEDULED'
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    EXPIRED = 'EXPIRED'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'


class DossierState(Enum):
    NOT_CONFIRMED = 'NOT_CONFIRMED'
    WAITING_SCORE_RESULTS = "WAITING_SCORE_RESULTS"
    WAITING_OPERATOR_CONFIRM = "WAITING_OPERATOR_CONFIRM"
    WAITING_OWNER_CONFIRM = "WAITING_OWNER_CONFIRM"
    COMPLETED = 'COMPLETED'
    REJECTED = "REJECTED"
    ERROR = "ERROR"


def create_request(request_uid, presentation_id, start_date: datetime, end_date: datetime,  dossier_id=None,
                   process_id=None,
                   verify_request_uid: str = None):

    request = IqpRequest.objects.create(request_uid=request_uid, start_date=start_date, end_date=end_date,
                                        status=RequestStatus.STARTED.value,
                                        dossier_id=dossier_id, process_id=process_id,
                                        verify_request_uid=verify_request_uid,
                                        presentation_id=presentation_id)

    return request


def __find_iqp_request(id: int = None, request_uid: str = None, status: RequestStatus = None,
                       dossier_id=None, verify_request_uid=None, process_id=None) -> IqpRequest:
    try:
        filters = dict()

        if id:
            filters['id'] = id
        if request_uid:
            filters['request_uid'] = request_uid
        if status:
            filters['status'] = status.value
        if dossier_id:
            filters['dossier_id'] = dossier_id
        if verify_request_uid:
            filters['verify_request_uid'] = verify_request_uid
        if process_id:
            filters['process_id'] = process_id

        iqp_request = IqpRequest.objects.filter(**filters)
    except ObjectDoesNotExist:
        iqp_request = None
    return iqp_request


def find_iqp_request_by_verify_request_uid(verify_request_uid: str):
    iqp_request = None
    results = __find_iqp_request(verify_request_uid=verify_request_uid)
    if results:
        iqp_request = results[0]

    return iqp_request


def find_iqp_request_by_process_id(process_id: str):
    iqp_request = None
    results = __find_iqp_request(process_id=process_id)
    if results:
        iqp_request = results[0]
    return iqp_request


def create_dossier(dossier_id, webid_request: IqpRequest, data, user_connection: UserConnection,
                   state=DossierState.NOT_CONFIRMED.value) -> IqpDossier:

    dossier = IqpDossier.objects.create(dossier_id=dossier_id, iqp_request=webid_request,
                                        data=data, state=state, user_connection=user_connection, reason=None,
                                        awaited_owner_confirmation=0,
                                        last_update_date=datetime_now())
    return dossier


def find_dossier_by_dossier_id(dossier_id) -> IqpDossier:
    try:
        iqp_dossier = IqpDossier.objects.get(dossier_id=dossier_id)
    except ObjectDoesNotExist:
        iqp_dossier = None
    return iqp_dossier


def update_dossier(dossier_id, data=None, state: str = None, reason=None, awaited_owner_confirmation: int = None):
    dossier = find_dossier_by_dossier_id(dossier_id)

    if dossier:
        if state:
            dossier.state = state
        if data:
            dossier.data = data
        if reason:
            dossier.reason = reason
        if awaited_owner_confirmation is not None:
            dossier.awaited_owner_confirmation = awaited_owner_confirmation

        dossier.last_update_date = datetime_now()
        dossier.save()

    return dossier
