from generic_organization_service.models import Request, Organization, UserConnection
from generic_organization_service.models import IssueRequest
from generic_organization_service.models import VerifyRequest
from generic_organization_service.models import ConnectionRequest

from django.core.exceptions import ObjectDoesNotExist
from enum import Enum
import datetime


class RequestType(Enum):
    ISSUE = 'ISSUE'
    REVOKE = 'REVOKE'
    VERIFY = 'VERIFY'
    CONNECTION = 'CONNECTION'
    MESSAGE = 'MESSAGE'
    GENERIC = 'GENERIC'


class RequestStatus(Enum):
    SCHEDULED = 'SCHEDULED'
    STARTED = 'STARTED'
    COMPLETED = 'COMPLETED'
    EXPIRED = 'EXPIRED'
    FAILED = 'FAILED'
    REJECTED = 'REJECTED'
    MULTIPLE_REQUEST_STARTED = "MULTIPLE_REQUEST_STARTED"


def create_request(request_uid, start_date: datetime, end_date: datetime, request_type, organization: Organization,
                   parent_request: Request = None):
    request = Request.objects.create(request_uid=request_uid, start_date=start_date,
                                     end_date=end_date, request_type=request_type,
                                     status=RequestStatus.STARTED.value, organization=organization,
                                     parent_request=parent_request)
    return request


def create_issue_request(request_uid, start_date: datetime, end_date: datetime, credential,
                         organization: Organization, parent_request: Request = None, user_connection=None,
                         values_for_credential=None,
                         issued_by_operator=False):

    request = IssueRequest.objects.create(request_uid=request_uid, start_date=start_date,
                                          end_date=end_date, request_type=RequestType.ISSUE.value,
                                          credential=credential, status=RequestStatus.STARTED.value,
                                          organization=organization, parent_request=parent_request,
                                          user_connection=user_connection,
                                          values_for_credential=values_for_credential,
                                          issued_by_operator=issued_by_operator)
    return request


def update_or_create_issue_request(request_uid, start_date: datetime, end_date: datetime, credential,
                                   organization: Organization, parent_request: Request = None,
                                   user_connection=None, values_for_credential=None,
                                   issued_by_operator=False):

    if values_for_credential is None:
        values_for_credential = {}

    request, created = IssueRequest.objects.update_or_create(
        request_uid=request_uid, start_date=start_date,
        end_date=end_date, request_type=RequestType.ISSUE.value,
        credential=credential, status=RequestStatus.STARTED.value,
        organization=organization, parent_request=parent_request,
        user_connection=user_connection,
        defaults={'values_for_credential': values_for_credential},
        issued_by_operator=issued_by_operator)
    return request


def update_issue_request(issue_request: IssueRequest = None, identifier_key: str = None,
                         discard_description: str = None, status: str = None):
    if identifier_key:
        issue_request = get_issue_request_by_identifier(identifier=identifier_key)

    if issue_request:
        if status:
            issue_request.status = status

        if discard_description:
            issue_request.discard_description = discard_description

        issue_request.save()
    return issue_request


def create_connection_request(request_uid, start_date: datetime, end_date: datetime, organization: Organization,
                              parent_request: Request = None, status: str = RequestStatus.STARTED.value,
                              allow_multiple_read=False, user_connection: UserConnection = None):

    request = ConnectionRequest.objects.create(request_uid=request_uid, start_date=start_date,
                                               end_date=end_date, request_type=RequestType.CONNECTION.value,
                                               status=status, organization=organization,
                                               parent_request=parent_request,
                                               allow_multiple_read=allow_multiple_read,
                                               user_connection=user_connection)
    return request


def create_verify_request(request_uid, start_date: datetime, end_date: datetime, proofserviceaction,
                          organization: Organization, allow_multiple_read=False, restrictions={},
                          parent_request: Request = None, status: str = RequestStatus.SCHEDULED.value,
                          user_connection: UserConnection = None):
    request = VerifyRequest.objects.create(request_uid=request_uid, start_date=start_date,
                                           end_date=end_date, request_type=RequestType.VERIFY.value,
                                           proof_service_action=proofserviceaction, status=status,
                                           organization=organization,
                                           allow_multiple_read=allow_multiple_read,
                                           restrictions=restrictions,
                                           parent_request=parent_request,
                                           user_connection=user_connection)
    return request


def list_requests(request_type):
    request = None

    if request_type == RequestType.ISSUE.value:
        request = IssueRequest.objects.all()
    elif request_type == RequestType.VERIFY.value:
        request = VerifyRequest.objects.all()
    else:
        request = Request.objects.all()

    return request


def get_request(request_uid=None, id=None, request_type=None, credential=None, user_connection=None,
                credential_business_code=None, user_business_uid=None, service=None, proof_business_code=None) \
        -> Request:
    try:
        filters = dict()
        if request_uid:
            filters['request_uid'] = request_uid
        if id:
            filters['id'] = id
        if request_type:
            filters['request_type'] = request_type
        if user_connection:
            filters['user_connection'] = user_connection
        if user_business_uid:
            filters['user__business_uid'] = user_business_uid
        # issue request
        if credential:
            filters['credential'] = credential
        if credential_business_code:
            filters['credential__business_code'] = credential_business_code
        # verify request
        if proof_business_code:
            filters['proof_service_action__proof__business_code'] = proof_business_code
        if service:
            filters['proof_service_action__service__name'] = service

        if request_type:
            if request_type == RequestType.ISSUE.value:
                request = IssueRequest.objects.get(**filters)
            elif request_type == RequestType.VERIFY.value:
                request = VerifyRequest.objects.get(**filters)
        else:
            request = Request.objects.get(**filters)
    except ObjectDoesNotExist:
        request = None
    return request


def get_issue_request(request_uid: str, credential_business_code: str = None,
                      user_connection: UserConnection = None) -> IssueRequest:
    try:
        filters = dict()
        if request_uid:
            filters['request_uid'] = request_uid
        if credential_business_code:
            filters['credential__business_code'] = credential_business_code
        if user_connection:
            filters['user_connection'] = user_connection

        request = IssueRequest.objects.get(**filters)

    except ObjectDoesNotExist:
        request = None
    return request


def get_verify_request_by_request_uid(request_uid: str) -> VerifyRequest:
    try:
        request = VerifyRequest.objects.get(request_uid=request_uid)
    except ObjectDoesNotExist:
        request = None
    return request


def get_connection_request_by_request_uid(request_uid: str) -> ConnectionRequest:
    try:
        request = ConnectionRequest.objects.get(request_uid=request_uid)
    except ObjectDoesNotExist:
        request = None
    return request


def get_verify_request(identifier=None) -> VerifyRequest:
    try:
        request = VerifyRequest.objects.get(request_ptr_id=identifier)
    except ObjectDoesNotExist:
        request = None
    return request


def get_issue_request_by_identifier(identifier=None) -> IssueRequest:
    try:
        request = IssueRequest.objects.get(request_ptr_id=identifier)
    except ObjectDoesNotExist:
        request = None
    return request


def set_request_status(status, request_uid=None, identifier=None, user_connection: UserConnection = None):
    request = get_request(request_uid=request_uid, id=identifier)
    if request:
        request.status = status
    if user_connection:
        request.user_connection = user_connection

        request.save()
    return request


def set_user_connection(user_connection: UserConnection, request_uid=None, identifier=None):
    request = get_request(request_uid=request_uid, id=identifier)

    if request:
        request.user_connection = user_connection
        request.save()
    return request
