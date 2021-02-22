import logging
import uuid
import datetime

from django.http import JsonResponse
from django.db import transaction as django_transaction

from antidote import register, inject
from generic_organization_service.interfaces.responses.generic_response import StatusCode, MessagesCode, \
    GenericResponse
from generic_organization_service.entity import user_entity, request_entity, organization_entity, agent_entity
from generic_organization_service.utils.description_handler import DescriptionHandler, DescriptionMessagesCodes
from generic_organization_service.handlers.organization_handler_manager import OrganizationHandlerManager
from generic_organization_service.interfaces.schemas.request_schemas import ConnectionNotifyRequestSchema, \
    StartConnectionRequestSchema
from generic_organization_service.interfaces.responses.connection_request_response import ConnectionRequestResponse
from generic_organization_service.interfaces.schemas.response_schemas import GenericResponseSchema, \
    ConnectionRequestResponseSchema
from generic_organization_service.entity.request_entity import RequestStatus
from generic_organization_service.utils import util

from agent_client.agent_client import DizmeAgentClient, AuthzLogin
from agent_client.interfaces.requests.connection_request import ConnectionRequest
from generic_organization import celery

logger = logging.getLogger(__name__)


@register(singleton=True)
class ConnectionService:

    @inject
    def __init__(self, description_handler: DescriptionHandler, handler_manager: OrganizationHandlerManager):
        self.description_handler = description_handler
        self.handler_manager = handler_manager

    def connection_notify(self, request_data: dict):
        logger.info("Connection notify requested")
        req_schema = ConnectionNotifyRequestSchema()
        data, errors = req_schema.load(request_data)

        if not errors:
            logger.debug("Connection notify Request Data => request data: %s ", str(request_data))
            request_uid = data['request_uid']
            connection_id = data['connection_id']
            try:
                request = request_entity.get_request(request_uid=request_uid)
                if request:
                    user_connection = user_entity.add_user_connection(connection_id, request.organization)
                    if request.request_type == request_entity.RequestType.CONNECTION.value:
                        conn_request = request_entity.get_connection_request_by_request_uid(request.request_uid)
                        if conn_request.allow_multiple_read:
                            request_uid = str(uuid.uuid1())
                            start_date = util.datetime_now()
                            request_entity.create_connection_request(
                                request_uid, start_date, None, request.organization,
                                status=RequestStatus.COMPLETED.value,
                                allow_multiple_read=conn_request.allow_multiple_read,
                                parent_request=request,
                                user_connection=user_connection)
                        else:
                            request_entity.set_request_status(request_entity.RequestStatus.COMPLETED.value,
                                                              request_uid=request_uid,
                                                              user_connection=user_connection)

                    celery.handle_connection_notify.delay(request.organization.name, request_uid, connection_id,
                                                          request_data)

                    confirm_response = GenericResponse(
                        StatusCode.SUCCESS,
                        MessagesCode.SUCCESS, "Ok!")
                else:
                    logger.warning("The request_uid: %s has not been found", request_uid)
                    confirm_response = GenericResponse(StatusCode.ERROR, MessagesCode.OPERATION_ERROR,
                                                       "Request not found")
            except Exception as e:
                logger.error("Exception during save connection: " + str(e))
                confirm_response = GenericResponse(StatusCode.ERROR, MessagesCode.OPERATION_ERROR,
                                                   str(e))
        else:
            logger.error("Invalid or missing data format in connection_notify: %s ", str(errors))
            confirm_response = GenericResponse(StatusCode.ERROR, MessagesCode.OPERATION_ERROR,
                                               str(errors))

        response_schema = GenericResponseSchema()
        result_data = response_schema.dump(confirm_response)
        return JsonResponse(result_data.data)

    def start_connection(self, request_data: dict):
        # Verify proof
        logger.info("Start connection requested")
        connection_request_schema = StartConnectionRequestSchema()
        data, errors = connection_request_schema.load(request_data)

        if not errors:
            try:
                logger.debug("Start connection request => request data: %s ", str(request_data))
                organization = organization_entity.get_organization_by_business_code(data['organization_business_code'])

                if organization:
                    agent = agent_entity.get_active_agent(organization)
                    agent_auth = AuthzLogin(**agent.auth)

                    agent_client = DizmeAgentClient(agent.ip_address, agent_auth)
                    multiple_read = data['allow_multiple_read']
                    request_uid = str(uuid.uuid1())

                    connection_request = ConnectionRequest(request_uid=request_uid, allow_multiple_read=multiple_read)
                    response = agent_client.connection_request(connection_request)

                    if response.status_code.is_success():
                        with django_transaction.atomic():
                            start_date = datetime.datetime.now()
                            request_entity.create_connection_request(request_uid, start_date, None,
                                                                     organization, allow_multiple_read=multiple_read)

                            request_verify_response = ConnectionRequestResponse(StatusCode.SUCCESS,
                                                                                MessagesCode.SUCCESS,
                                                                                "Connection request success")
                            invitations = [
                                 {
                                    "invitation_short_link": response.get_invitation_short_link()
                                 }
                            ]
                            request_verify_response.set_invitations(invitations)

                    else:
                        logger.error("Error on get connection invitation")
                        request_verify_response = GenericResponse(StatusCode.ERROR,
                                                                  MessagesCode.OPERATION_ERROR,
                                                                  "Connection invitation failed: " + str(request_data))
                else:
                    logger.warning("Organization not found with provided code")
                    request_verify_response = GenericResponse(StatusCode.ERROR,
                                                              MessagesCode.OPERATION_ERROR,
                                                              "Organization not found: " + str(request_data))
            except Exception as oe:
                logger.error("Exception during start connection request ", str(oe))
                request_verify_response = ConnectionRequestResponse(
                    StatusCode.ERROR, MessagesCode.OPERATION_ERROR, str(oe))
        else:
            logger.error("Invalid or missing data format in start connection request: %s ", str(errors))
            request_verify_response = ConnectionRequestResponse(StatusCode.ERROR, MessagesCode.OPERATION_ERROR,
                                                                "Invalid value for connection request params: "
                                                                + str(errors))

        response_schema = ConnectionRequestResponseSchema()
        result_data = response_schema.dump(request_verify_response)
        return JsonResponse(result_data.data)
