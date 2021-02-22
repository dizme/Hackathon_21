from generic_organization_service.models import WebIdRequest, WebIdDossier, UserConnection
from generic_organization_service.utils.util import datetime_now
from enum import Enum
from django.core.exceptions import ObjectDoesNotExist
import datetime


class RequestType(Enum):
    WITH_DOC = 'WITH_DOC'
    WITHOUT_DOC = 'WITHOUT_DOC'
    SPID_L2 = 'SPID_L2'


class RequestStatus(Enum):
    SCHEDULED = 'SCHEDULED'
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    EXPIRED = 'EXPIRED'
    FAILED = 'FAILED'
    SUCCESS = 'SUCCESS'


class DossierState(Enum):
    NOT_CONFIRMED = 'NOT_CONFIRMED'
    CONFIRMED = 'CONFIRMED'
    ERROR = 'ERROR'
    ABORTED = 'ABORTED'
    COMPLETED = 'COMPLETED'
    DORMANT = 'DORMANT'
    RUNNING = 'RUNNING'
    PENDING_COMPLETION = 'PENDING_COMPLETION'


def create_request(request_uid, presentation_id, start_date: datetime, end_date: datetime, request_type,
                   dossier_id=None, verify_request_uid: str = None):

    request = WebIdRequest.objects.create(request_uid=request_uid, start_date=start_date, end_date=end_date,
                                          request_type=request_type, status=RequestStatus.STARTED.value,
                                          dossier_id=dossier_id, verify_request_uid=verify_request_uid,
                                          presentation_id=presentation_id)

    return request


def update_request_status(id, request_uid, status: RequestStatus, end_date: datetime):
    requests = find_webid_request(id, request_uid)
    request = None
    if requests:
        request = requests[0]

    request.status = status.value
    if end_date:
        request.end_date = end_date
    request.save()
    return request


def find_webid_request(id: int = None, request_uid: str = None,
                       status: RequestStatus = None, dossier_id=None) -> WebIdRequest:
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

        webid_request = WebIdRequest.objects.filter(**filters)
    except ObjectDoesNotExist:
        webid_request = None
    return webid_request


def create_dossier(dossier_id, webid_request: WebIdRequest, data, user_connection: UserConnection,
                   token_link) -> WebIdDossier:

    dossier = WebIdDossier.objects.create(dossier_id=dossier_id, webid_request=webid_request,
                                          data=data, state=DossierState.NOT_CONFIRMED.value,
                                          user_connection=user_connection, reason=None,
                                          token_link=token_link, last_update_date=datetime_now())
    return dossier


def find_dossier(dossier_id=None, webid_request: WebIdDossier = None,
                 state: DossierState = None):
    try:
        filters = dict()

        if id:
            filters['dossier_id'] = dossier_id
        if webid_request:
            filters['webid_request'] = webid_request
        if state:
            filters['state'] = state.value

        webid_request = WebIdRequest.objects.filter(**filters)
    except ObjectDoesNotExist:
        webid_request = None
    return webid_request


def find_dossier_by_dossier_id(dossier_id) -> WebIdDossier:
    try:
        webid_request = WebIdDossier.objects.get(dossier_id=dossier_id)
    except ObjectDoesNotExist:
        webid_request = None
    return webid_request


def update_dossier(dossier_id, data, state: str, reason):
    dossier = find_dossier_by_dossier_id(dossier_id)

    if dossier:
        dossier.state = state
        dossier.data = data
        dossier.reason = reason
        dossier.last_update_date = datetime_now()

        dossier.save()

    return dossier

