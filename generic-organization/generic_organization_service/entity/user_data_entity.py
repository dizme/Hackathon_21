from generic_organization_service.models import Agent, Organization, UserConnection, UserData, \
    WebIdUserData, WebIdRequest, IqpUserData, VerifyRequest, Request
from django.core.exceptions import ObjectDoesNotExist
from enum import Enum


class DataSource(Enum):
    IDCHECK = 'IDCHECK'
    WEB_ID = 'WEB_ID'
    VERIFY = 'VERIFY'
    EXTERNAL = "EXTERNAL"

    def __str__(self):
        return self.value


def insert_data(user_connection: UserConnection, data: dict, source: DataSource, type: str,
                request: Request = None) -> UserConnection:

    user_data = UserData.objects.create(user_connection=user_connection, data=data,
                                        source=source.value, type=type, request=request)
    return user_data


def store_verify_data(user_connection: UserConnection, data: dict, type: str, verify_request: VerifyRequest) -> \
        UserData:
    user_data = UserData.objects.update_or_create(user_connection=user_connection, source=str(DataSource.VERIFY.value),
                                                  type=type, request=verify_request, defaults={'data': data},)
    return user_data


def insert_data_from_webid(user_connection: UserConnection, data: dict, type:str, verify_request: VerifyRequest,
                           webid_request: WebIdRequest) -> WebIdUserData:
    user_data = WebIdUserData.objects.create(user_connection=user_connection, data=str(data),
                                             source=str(DataSource.VERIFY.value),
                                             type=type, request=verify_request, webid_request=webid_request)
    return user_data


def insert_data_from_iqp(user_connection: UserConnection, data: dict, type: str, verify_request: VerifyRequest,
                         webid_request: WebIdRequest) -> WebIdUserData:

    user_data = IqpUserData.objects.create(user_connection=user_connection, data=str(data),
                                           source=str(DataSource.VERIFY.value),
                                           type=type, request=verify_request, iqp_request=webid_request)
    return user_data


def get_data(user_connection: UserConnection = None, data: dict = None, source: DataSource = None, type: str = None):
    try:
        filters = dict()

        if user_connection:
            filters['user_connection'] = user_connection
        if data:
            filters['data'] = data
        if source:
            filters['source'] = source
        if type:
            filters['type'] = type

        user_data = UserData.objects.filter(**filters)
    except ObjectDoesNotExist:
        user_data = None
    return user_data


def get_data_from_request(user_connection: UserConnection = None, data: dict = None,
                          type: str = None, request: Request = None, request_uid: str = None) -> \
        UserData:
    try:
        filters = dict()

        if user_connection:
            filters['user_connection'] = user_connection
        if data:
            filters['data'] = data
        if type:
            filters['type'] = type
        if request:
            filters['request'] = request
        if request_uid:
            filters['request__request_uid'] = request_uid

        user_data = UserData.objects.filter(**filters)
    except ObjectDoesNotExist:
        user_data = None
    return user_data
