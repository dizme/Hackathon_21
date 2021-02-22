import logging
import json
import uuid
import datetime

from django.http import JsonResponse
from antidote import register, inject
from django.db import transaction as django_transaction

from django.template.loader import get_template
from django.http import HttpResponse
from generic_organization.settings import VERIFY_WIDGET_URL, VERIFY_WIDGET_REQUEST_CONTEXT
from agent_client.agent_client import AuthzLogin, DizmeAgentClient
from agent_client.interfaces.requests.verify_request import VerifyRequest
from generic_organization_service.interfaces.schemas.request_schemas import StartVerifyRequestSchema
from generic_organization_service.interfaces.schemas.response_schemas import VerifyRequestResponseSchema
from generic_organization_service.interfaces.responses.verify_request_response import VerifyRequestResponse
from generic_organization_service.interfaces.responses.generic_response import StatusCode, MessagesCode, \
    GenericResponse, VerifyResult
from generic_organization_service.entity import proof_service_action_entity, agent_entity, request_entity, \
    user_entity, user_data_entity, verify_confirm_entity
from generic_organization_service.entity.verify_confirm_entity import VerifyStatus
from generic_organization_service.exception.operation_error import OperationError
from generic_organization_service.interfaces.schemas.request_schemas import ConfirmVerifyRequestSchema
from generic_organization_service.interfaces.schemas.response_schemas import ConfirmVerifyResponseSchema
from generic_organization_service.interfaces.schemas.request_schemas import DiscardProofRequestSchema
from generic_organization_service.utils.description_handler import DescriptionHandler, DescriptionMessagesCodes
from generic_organization_service.interfaces.responses.confirm_verify_response import ConfirmVerifyResponse
from generic_organization_service.models import VerifyRequest as VerifyRequestModel
from generic_organization_service.handlers.organization_handler_manager import OrganizationHandlerManager
from generic_organization_service.entity.request_entity import RequestStatus
from generic_organization_service.interfaces.schemas.response_schemas import GenericResponseSchema
from generic_organization_service.utils import util
from generic_organization import celery

logger = logging.getLogger(__name__)


@register(singleton=True)
class VerifyService:

    @inject
    def __init__(self, description_handler: DescriptionHandler, handler_manager: OrganizationHandlerManager):
        self.description_handler = description_handler
        self.handler_manager = handler_manager

    def start_verify(self, request_data: dict):
        # Verify proof
        logger.info("Start verify requested")
        confirm_verify_schema = StartVerifyRequestSchema()
        data, errors = confirm_verify_schema.load(request_data)

        if not errors:
            try:
                logger.debug("Start verify Data => request data: %s ", str(request_data))
                proof_service_action = proof_service_action_entity.get_proof_service_action(
                    proof_business_code=data['proof_business_code'],
                    service_name=data['service'])
                if proof_service_action:
                    organization = proof_service_action.proof.organization
                    agent = agent_entity.get_active_agent(organization)
                    agent_auth = AuthzLogin(**agent.auth)

                    agent_client = DizmeAgentClient(agent.ip_address, agent_auth)
                    multiple_read = data['allow_multiple_read']
                    request_uid = str(uuid.uuid1())

                    verify_request = VerifyRequest(proof_service_action.proof.business_code)
                    verify_request.set_request_uid(request_uid)
                    verify_request.set_allow_multiple_read(multiple_read)

                    response = agent_client.verify_request(verify_request)

                    if response.status_code.is_success():
                        with django_transaction.atomic():
                            start_date = datetime.datetime.now()
                            request_entity.create_verify_request(request_uid, start_date, None, proof_service_action,
                                                                 organization, multiple_read, data['restrictions'])

                            request_verify_response = VerifyRequestResponse(StatusCode.SUCCESS,
                                                                            MessagesCode.SUCCESS,
                                                                            "Verify request success")
                            invitations = [
                                 {
                                    "invitation_short_link": response.get_invitation_short_link()
                                 }
                            ]
                            request_verify_response.set_invitations(invitations)

                            logger.info("New verify request : %s", request_uid)
                    else:
                        logger.error("Error on get proof invitation")
                        request_verify_response = GenericResponse(StatusCode.ERROR,
                                                                  MessagesCode.OPERATION_ERROR,
                                                                  "Verify proof request on failure: " + str(request_data))
                else:
                    logger.warning("Proof not found with provided code and service")
                    request_verify_response = GenericResponse(StatusCode.ERROR,
                                                              MessagesCode.OPERATION_ERROR,
                                                              "Proof request not found: " + str(request_data))
            except OperationError as oe:
                logger.error("Exception during start verify request ", str(oe))
                request_verify_response = VerifyRequestResponse(StatusCode.ERROR,
                                                                MessagesCode.OPERATION_ERROR,
                                                                str(oe))
        else:
            logger.error("Invalid or missing data format in start verify request: %s ", str(errors))
            request_verify_response = VerifyRequestResponse(StatusCode.ERROR,
                                                            MessagesCode.OPERATION_ERROR,
                                                            "Invalid value for verify request params: " + str(
                                                                errors))

        response_schema = VerifyRequestResponseSchema()
        result_data = response_schema.dump(request_verify_response)
        return JsonResponse(result_data.data)

    def start_verify_with_widget(self, request_data: dict):
        # Verify proof
        logger.info("Start verify with widget requested")
        confirm_verify_schema = StartVerifyRequestSchema()
        data, errors = confirm_verify_schema.load(request_data)

        if not errors:
            try:
                logger.debug("Start verify with widget => request data: %s ", str(request_data))
                proof_service_action = proof_service_action_entity.get_proof_service_action(
                    proof_business_code=data['proof_business_code'],
                    service_name=data['service'])

                organization = proof_service_action.proof.organization
                multiple_read = data['allow_multiple_read']
                request_uid = str(uuid.uuid1())

                with django_transaction.atomic():
                    start_date = datetime.datetime.now()
                    request_entity.create_verify_request(request_uid, start_date, None,
                                                         proof_service_action,
                                                         organization, multiple_read, data['restrictions'])
                    t = get_template('main.html')
                    data_to_redender = {}
                    data_to_redender.update({'proof_business_code': data['proof_business_code'],
                                             'orgid': organization,
                                             'multiple_read': multiple_read,
                                             'restrictions': data['restrictions'],
                                             'widget_url': VERIFY_WIDGET_URL,
                                             'request_context': VERIFY_WIDGET_REQUEST_CONTEXT,
                                             'request_uid': request_uid})
                    html = t.render(data_to_redender)
                    return HttpResponse(html)

            except OperationError as oe:
                logger.error("Exception during start verify credential ", str(oe))
                request_verify_response = VerifyRequestResponse(StatusCode.ERROR,
                                                                MessagesCode.OPERATION_ERROR,
                                                                str(oe))
        else:
            logger.error("Invalid or missing data format in start verify request: %s ", str(errors))
            request_verify_response = VerifyRequestResponse(
                StatusCode.ERROR, MessagesCode.OPERATION_ERROR,
                "Invalid value for credential request params: " + str(errors))

        response_schema = VerifyRequestResponseSchema()
        result_data = response_schema.dump(request_verify_response)
        return JsonResponse(result_data.data)

    def confirm_verify(self, request_data: dict):
        logger.info("confirm verify requested")
        confirm_verify_schema = ConfirmVerifyRequestSchema()
        data, errors = confirm_verify_schema.load(request_data)

        if not errors:
            try:

                logger.info("Confirm verify request_uid: %s proof_business_code %s",
                            data['request_uid'],
                            data['proof_business_code'])

                request_valid, verify_request = self.__validate_verify_request(data['request_uid'],
                                                                               data['proof_business_code'])
                if request_valid:
                    return self.handle_confirm_verify(verify_request, data)
                else:
                    logger.error("The data provided: %s is not related to a valid Verify Request or has"
                                 " not been found", str(data['request_uid']))
                    confirm_response = ConfirmVerifyResponse(StatusCode.ERROR,
                                                             MessagesCode.OPERATION_ERROR,
                                                             "Request not found: " + str(data['request_uid']))

                    descriptions = self.description_handler.get_descriptions(
                        DescriptionMessagesCodes.ERROR_DURING_VERIFY)
                    confirm_response.set_descriptions(descriptions)
                    confirm_response.set_send_response(True)

            except OperationError as oe:
                logger.error("Exception during confirm_verify ", str(oe))
                confirm_response = ConfirmVerifyResponse(StatusCode.ERROR,
                                                         MessagesCode.OPERATION_ERROR,
                                                         str(oe))
                descriptions = self.description_handler.get_descriptions(
                    DescriptionMessagesCodes.ERROR_DURING_VERIFY)
                confirm_response.set_descriptions(descriptions)
                confirm_response.set_send_response(True)
        else:
            logger.error("Invalid or missing data format in confirm verify request: %s ", str(errors))
            confirm_response = ConfirmVerifyResponse(StatusCode.ERROR,
                                                     MessagesCode.OPERATION_ERROR,
                                                     "Invalid value for credential request params: " + str(errors))

            descriptions = self.description_handler.get_descriptions(
                DescriptionMessagesCodes.ERROR_DURING_VERIFY_CONTACT_SUPPORT)
            confirm_response.set_descriptions(descriptions)
            confirm_response.set_send_response(True)

        response_schema = ConfirmVerifyResponseSchema()
        result_data = response_schema.dump(confirm_response)
        return JsonResponse(result_data.data)

    def handle_confirm_verify(self, verify_request_model: VerifyRequestModel, data: dict):
        logger.info("handle_confirm_verify")
        try:
            multiple_read_allowed = verify_request_model.allow_multiple_read
            presentation_id = data['presentation_id']
            request_uid = verify_request_model.request_uid
            with django_transaction.atomic():
                proof_service_action = verify_request_model.proof_service_action
                connection_id = data['connection_id']
                # store user connection if any
                user_connection = user_entity.add_user_connection(connection_id, verify_request_model.organization)

                verify_data = dict()
                verify_data.update(data['revealed_attributes'])
                verify_data.update(data['unrevealed_attributes'])
                verify_data.update(data['self_attested_attributes'])
                verify_data['presentation_id'] = presentation_id

                data['presentation_id'] = presentation_id

                verify_request_ref = verify_request_model
                if multiple_read_allowed:
                    verify_request_model.status = request_entity.RequestStatus.MULTIPLE_REQUEST_STARTED.value
                    request_uid = str(uuid.uuid1())
                    start_date = util.datetime_now()
                    verify_request_ref = request_entity.create_verify_request(
                        request_uid, start_date, None, proof_service_action,
                        verify_request_model.organization,
                        multiple_read_allowed, verify_request_model.restrictions,
                        parent_request=verify_request_model,
                        status=RequestStatus.COMPLETED.value,
                        user_connection=user_connection)
                else:
                    verify_request_model.status = request_entity.RequestStatus.COMPLETED.value

                user_data_entity.store_verify_data(user_connection=user_connection,
                                                   data=verify_data,
                                                   type=None, verify_request=verify_request_ref)

                verify_confirm_entity.create_verify_confirm(verify_request=verify_request_ref,
                                                            confirm_date=util.datetime_now(),
                                                            verify_status=VerifyStatus.COMPLETED,
                                                            proof_evidence=json.dumps(data['proof']),
                                                            proof_request=data['proof_request'],
                                                            user_connection=user_connection)

                request_entity.set_request_status(status=verify_request_model.status,
                                                  request_uid=verify_request_model.request_uid,
                                                  user_connection=(user_connection if not multiple_read_allowed
                                                                   else None))

                send_response = True
                org_handler = self.handler_manager.get_organization_handler(verify_request_model.organization.name)

                if org_handler:
                    logger.info("For the request_uid: %s the processing will "
                                "continue with properly organization handler",
                                request_uid)
                    celery.handle_verify_confirm.delay(verify_request_model.organization.name, request_uid,
                                                       connection_id, presentation_id, data)
                    send_response = False

                confirm_response = ConfirmVerifyResponse(StatusCode.SUCCESS,
                                                         MessagesCode.SUCCESS,
                                                         "Success!")

                confirm_response.set_verify_result(VerifyResult.OK)
                confirm_response.set_send_response(send_response)

        except OperationError as oe:
            logger.error("Exception during values for credential ", str(oe))
            confirm_response = ConfirmVerifyResponse(StatusCode.ERROR, MessagesCode.OPERATION_ERROR, str(oe))
            descriptions = self.description_handler.get_descriptions(
                DescriptionMessagesCodes.ERROR_DURING_VERIFY_CONTACT_SUPPORT)
            confirm_response.set_descriptions(descriptions)
            confirm_response.set_send_response(True)

        response_schema = ConfirmVerifyResponseSchema()
        result_data = response_schema.dump(confirm_response)
        return JsonResponse(result_data.data)

    def discard_proof(self, request_data: dict):
        logger.info("Discard proof requested")
        req_schema = DiscardProofRequestSchema()
        data, errors = req_schema.load(request_data)

        if not errors:
            logger.debug("Discard Proof Request Data => request data: %s ", json.dumps(request_data))

            request_uid = data['request_uid']
            connection_id = data['connection_id']

            logger.info("Discard proof for request uid : %s for connection_id %s ",
                        str(request_uid), connection_id)

            verify_request = request_entity.get_verify_request_by_request_uid(request_uid)
            if verify_request:
                try:
                    with django_transaction.atomic():

                        discard_response = GenericResponse(StatusCode.SUCCESS, MessagesCode.SUCCESS,
                                                           "Success!")
                        if not verify_request.allow_multiple_read:
                            request_entity.set_request_status(request_entity.RequestStatus.REJECTED.value,
                                                              request_uid=request_uid)

                        celery.handle_discard_proof.delay(verify_request.organization.name,
                                                          verify_request.request_uid,
                                                          connection_id, request_data)
                except ValueError as ie:
                    discard_response = GenericResponse(
                        StatusCode.ERROR,
                        MessagesCode.OPERATION_ERROR, str(ie))
            else:
                logger.error("Request not found with data provided request_uid: %s ", request_uid)
                discard_response = GenericResponse(
                    StatusCode.ERROR,
                    MessagesCode.OPERATION_ERROR,
                    "Proof discard not allowed, the request has not been found")
        else:
            logger.error("Invalid or missing data format in discard_credential: %s ", str(errors))
            discard_response = GenericResponse(
                StatusCode.ERROR,
                MessagesCode.OPERATION_ERROR,
                "Invalid discard proof request params: " + str(errors))

        response_schema = GenericResponseSchema()
        result_data = response_schema.dump(discard_response)
        return JsonResponse(result_data.data)

    def __validate_verify_request(self, request_uid: str, proof_business_code: str) -> VerifyRequest:
        unavailable_state_for_single_read = [request_entity.RequestStatus.COMPLETED.value,
                                             request_entity.RequestStatus.FAILED.value,
                                             request_entity.RequestStatus.EXPIRED.value]

        request = request_entity.get_request(request_uid=request_uid,
                                             request_type=request_entity.RequestType.VERIFY.value,
                                             proof_business_code=proof_business_code)
        if request:
            if request.allow_multiple_read or (request.status not in unavailable_state_for_single_read):
                return True, request
        return False, None