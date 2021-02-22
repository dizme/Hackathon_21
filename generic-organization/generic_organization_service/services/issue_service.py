import logging
import json
import uuid
import datetime

from django.http import JsonResponse
from antidote import register, inject
from django.db import transaction as django_transaction

from generic_organization_service.interfaces.responses.generic_response import StatusCode, MessagesCode, \
    GenericResponse
from generic_organization_service.interfaces.schemas.response_schemas import GenericResponseSchema

from generic_organization_service.utils.description_handler import DescriptionHandler, DescriptionMessagesCodes
from generic_organization_service.interfaces.schemas.request_schemas import ConfirmIssueRequestSchema
from generic_organization_service.handlers.organization_handler_manager import OrganizationHandlerManager
from generic_organization_service.entity import request_entity, user_entity, issued_credential_entity, agent_entity
from generic_organization_service.interfaces.schemas.request_schemas import DiscardCredentialRequestSchema, \
    ValuesForCredentialRequestSchema
from generic_organization_service.models import IssueRequest
from generic_organization_service.interfaces.schemas.response_schemas import ValuesForCredentialResponseSchema
from generic_organization_service.interfaces.responses.value_for_credential_response import ValueForCredentialResponse
from generic_organization_service.exception.issue_credential_exception import IssueCredentialException
from agent_client.agent_client import AuthzLogin, DizmeAgentClient
from agent_client.interfaces.requests.issue_credential_request import IssueCredentialRequest
from generic_organization import celery

logger = logging.getLogger(__name__)


@register(singleton=True)
class IssueService:

    @inject
    def __init__(self, description_handler: DescriptionHandler, handler_manager: OrganizationHandlerManager):
        self.description_handler = description_handler
        self.handler_manager = handler_manager

    def confirm_issue(self, request_data: dict):
        logger.info("Confirm Issue requested")
        req_schema = ConfirmIssueRequestSchema()
        data, errors = req_schema.load(request_data)

        if not errors:
            logger.debug("Confirm Issue Request Data => request data: %s ", json.dumps(request_data))
            request_uid = data['request_uid']
            credential_business_code = data['credential_def_id']
            connection_id = data['connection_id']

            logger.info("Confirm Issue for request uid : %s, for credential_code %s to connection_id: %s",
                        str(request_uid), credential_business_code, connection_id)

            user_connection, issue_request = self.validate_issue_request(request_uid, connection_id,
                                                                         credential_business_code)
            if user_connection and issue_request:
                try:
                    with django_transaction.atomic():
                        logger.info("Credential %s issued to connection_id: %s", credential_business_code,
                                    connection_id)

                        confirm_response = GenericResponse(StatusCode.SUCCESS, MessagesCode.SUCCESS, "Success!")

                        issued_credential_entity.create_issued_credential(issue_request, user_connection,
                                                                          issue_request.credential)

                        request_entity.set_request_status(request_entity.RequestStatus.COMPLETED.value,
                                                          identifier=issue_request.id)

                        celery.handle_confirm_issue.delay(issue_request.organization.name,
                                                          issue_request.request_uid,
                                                          connection_id,
                                                          request_data)

                except ValueError as ie:
                    confirm_response = GenericResponse(
                        StatusCode.ERROR,
                        MessagesCode.OPERATION_ERROR, str(ie))
            else:
                logger.error("Confirm issue not allowed, request not found with data provided for request_uid: %s ",
                             request_uid)

                confirm_response = GenericResponse(
                    StatusCode.ERROR,
                    MessagesCode.OPERATION_ERROR,
                    "Credential Issue Request has not been found")
        else:
            logger.error("Invalid or missing data format in confirm_issue: %s ", str(errors))
            confirm_response = GenericResponse(
                StatusCode.ERROR,
                MessagesCode.OPERATION_ERROR,
                "Invalid values for credential request params: " + str(errors))

        response_schema = GenericResponseSchema()
        result_data = response_schema.dump(confirm_response)
        return JsonResponse(result_data.data)

    def discard_credential(self, request_data: dict):
        logger.info("Discard credential requested")
        req_schema = DiscardCredentialRequestSchema()
        data, errors = req_schema.load(request_data)

        if not errors:
            logger.debug("Discard Credential Request Data => request data: %s ", json.dumps(request_data))

            request_uid = data['request_uid']
            credential_business_code = data['credential_def_id']
            connection_id = data['connection_id']
            description = data['description']

            logger.info("Discard Credential for request uid : %s for credential_code %s ",
                        str(request_uid), credential_business_code)
            logger.debug("for connection_id :%s", connection_id)

            user_connection, issue_request = self.validate_issue_request(request_uid, connection_id,
                                                                         credential_business_code)
            if user_connection and issue_request:
                try:
                    with django_transaction.atomic():
                        logger.info("Credential %s discarded for request_uid: %s",
                                    credential_business_code, request_uid)

                        confirm_response = GenericResponse(StatusCode.SUCCESS, MessagesCode.SUCCESS,
                                                           "Success!")

                        request_entity.update_issue_request(issue_request=issue_request,
                                                            discard_description=description,
                                                            status=request_entity.RequestStatus.REJECTED.value)

                        celery.handle_discard_credential.delay(issue_request.organization.name,
                                                               issue_request.request_uid,
                                                               connection_id,
                                                               request_data)
                except ValueError as ie:
                    confirm_response = GenericResponse(
                        StatusCode.ERROR,
                        MessagesCode.OPERATION_ERROR, str(ie))
            else:
                logger.error("Request not found with data provided request_uid: %s ", request_uid)
                confirm_response = GenericResponse(
                    StatusCode.ERROR,
                    MessagesCode.OPERATION_ERROR,
                    "Credential Discard Request has not been found")
        else:
            logger.error("Invalid or missing data format in discard_credential: %s ", str(errors))
            confirm_response = GenericResponse(
                StatusCode.ERROR,
                MessagesCode.OPERATION_ERROR,
                "Invalid values for credential request params: " + str(errors))

        response_schema = GenericResponseSchema()
        result_data = response_schema.dump(confirm_response)
        return JsonResponse(result_data.data)

    def values_for_credential(self, request_data: dict):
        request_schema = ValuesForCredentialRequestSchema()
        data, errors = request_schema.load(request_data)
        logger.info("Values for credential requested")

        if not errors:
            try:
                logger.debug("Values for credential request data: %s", json.dumps(request_data))
                request_uid = data['request_uid']
                parent_request_uid = data.get('parent_request_uid', None)
                credential_business_code = data['credential_def_id']
                connection_id = data['connection_id']

                logger.info(
                    "Values for credential for request uid : %s, with parent_request_uid : %s , for credential %s ",
                    str(request_uid), str(parent_request_uid), credential_business_code)

                user_connection, issue_request = self.validate_issue_request(request_uid, connection_id,
                                                                             credential_business_code)
                if user_connection and issue_request:

                    org_handler = self.handler_manager.get_organization_handler(issue_request.organization.name)

                    if org_handler:
                        logger.info("For the request_uid: %s the processing will continue "
                                    "with properly organization handler")

                        values_response = ValueForCredentialResponse(StatusCode.SUCCESS,
                                                                     MessagesCode.SUCCESS,
                                                                     "Success!")

                        credential_values = org_handler.handle_values_for_credential(
                             request_uid, connection_id, data)
                        values_response.set_credential_values(credential_values)
                        values_response.set_credential_def_id(credential_business_code)
                    else:
                        values_response = ValueForCredentialResponse(StatusCode.ERROR, MessagesCode.OPERATION_ERROR,
                                                                     "Handler not found for the the organization")
                else:
                    logger.error("The request_uid provided: %s is not related to an Issue Request or has"
                                 " not been found", request_uid)
                    values_response = ValueForCredentialResponse(StatusCode.ERROR, MessagesCode.OPERATION_ERROR,
                                                                 "Request not found")

            except ValueError as oe:
                logger.error("Exception during values for credential ", str(oe))
                values_response = ValueForCredentialResponse(StatusCode.ERROR,
                                                             MessagesCode.OPERATION_ERROR,
                                                             str(oe))
        else:
            logger.error("Invalid or missing data format in value for credential request: %s ", str(errors))
            values_response = ValueForCredentialResponse(StatusCode.ERROR,
                                                         MessagesCode.OPERATION_ERROR,
                                                         "Invalid value for credential request params: " + str(errors))

        response_schema = ValuesForCredentialResponseSchema()
        result_data = response_schema.dump(values_response)
        return JsonResponse(result_data.data)

    def issue_credential_from_issue_request(self, issue_request: IssueRequest):
        logger.info("issue_credential_from_issue_request")

        agent = agent_entity.get_active_agent(issue_request.organization)
        agent_auth = AuthzLogin(**agent.auth)
        dizme_agent_client = DizmeAgentClient(agent.ip_address, agent_auth)

        request_uid = str(issue_request.request_uid)
        logger.info("Request Send invitation for issue request with id %s, at organization %s "
                    "for credential %s user_connection: %s", request_uid, issue_request.organization.name,
                    issue_request.credential.name, issue_request.user_connection.connection_id)

        issue_credential_request = IssueCredentialRequest(issue_request.request_uid, issue_request.organization.name,
                                                          issue_request.credential.business_code)

        logger.error("Request_uid: %s -> user connection not found for user_connection: %s", issue_request.request_uid,
                     issue_request.user_connection.connection_id)

        issue_credential_request.set_connection_id(issue_request.user_connection.connection_id)
        issue_credential_request.set_credential_values(issue_request.values_for_credential)

        credential_issue_invitation_response = dizme_agent_client.issue_credential_request(issue_credential_request)

        if credential_issue_invitation_response.status_code.is_failure():
            logger.error("Issue request not accepted error message: %s", credential_issue_invitation_response.message)
            raise IssueCredentialException(StatusCode.ERROR, MessagesCode.OPERATION_ERROR,
                                           DescriptionMessagesCodes.ERROR_DURING_ISSUE_CONTACT_SUPPORT)

    def validate_issue_request(self, request_uid: str, connection_id: str,
                               credential_business_code: str):
        issue_request = None
        user_connection = user_entity.get_user_connection(connection_id=connection_id)
        if user_connection:
            issue_request = request_entity.get_issue_request(
                request_uid=request_uid, credential_business_code=credential_business_code,
                user_connection=user_connection)

        return user_connection, issue_request
