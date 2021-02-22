import logging

from agent_client.agent_client import DizmeAgentClient
from agent_client.utils.request_utils import AuthzLogin
from agent_client.interfaces.requests.verify_response_request import VerifyResponseRequest
from agent_client.interfaces.requests.send_notify_request import SendNotifyRequest
from generic_organization_service.interfaces.responses.generic_response import VerifyResult
from generic_organization_service.entity import agent_entity
from generic_organization_service.models import UserConnection
from antidote import register

logger = logging.getLogger(__name__)


@register(singleton=True)
class NotificationService:

    def send_notify_message_to_connection(self, user_connection: UserConnection, mime_type: str, title: list,
                                          body: list):
        logger.info("send_notification_message_to_user")

        connection_id = user_connection.connection_id

        logger.debug("send_notification_message_to_user having connection_id: %s", connection_id)

        agent = agent_entity.get_active_agent(user_connection.organization)
        agent_auth = AuthzLogin(**agent.auth)

        dizme_agent_client = DizmeAgentClient(agent.ip_address, agent_auth)

        notify_request = SendNotifyRequest(user_connection.connection_id, mime_type, title, body)
        notify_response = dizme_agent_client.send_notify(notify_request)

        return notify_response

    def send_verify_response(self, user_connection: UserConnection, presentation_id, description_list: list,
                             verify_result: VerifyResult):
        logger.info("send_verify_response to user: %s for presentation_id: %s", user_connection.connection_id,
                    presentation_id)

        agent = agent_entity.get_active_agent(user_connection.organization)
        agent_auth = AuthzLogin(**agent.auth)

        dizme_agent_client = DizmeAgentClient(agent.ip_address, agent_auth)

        verify_response = VerifyResponseRequest(presentation_id)
        verify_response.set_descriptions(description_list)
        verify_response.set_verify_result(verify_result.value)
        generic_response = dizme_agent_client.send_verify_response(verify_response)
        return generic_response
