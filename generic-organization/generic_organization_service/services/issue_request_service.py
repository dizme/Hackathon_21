import logging
import json

from agent_client.agent_client import DizmeAgentClient
from agent_client.utils.request_utils import AuthzLogin
from generic_organization_service.models import IssueRequest
from generic_organization_service.exception.issue_credential_exception import IssueCredentialException
from generic_organization_service.entity import agent_entity
from generic_organization_service.entity import user_entity
from agent_client.interfaces.requests.issue_credential_request import IssueCredentialRequest
from generic_organization_service.utils.description_handler import DescriptionMessagesCodes
from generic_organization_service.interfaces.responses.generic_response import StatusCode, MessagesCode


logger = logging.getLogger(__name__)


def issue_credential_from_issue_request(issue_request: IssueRequest):
    logger.info("issue_credential_from_issue_request")

    agent = agent_entity.get_active_agent(issue_request.organization)
    agent_auth = AuthzLogin(**agent.auth)

    dizme_agent_client = DizmeAgentClient(agent.ip_address, agent_auth)
    request_uid = str(issue_request.request_uid)

    logger.info("Request Send invitation for issue request with id %s, at organization %s "
                "for credential %s, user_connection: %s",  request_uid, issue_request.organization.name,
                issue_request.credential.name, issue_request.user_connection.connection_id)

    issue_credential_request = IssueCredentialRequest(issue_request.credential.business_code)

    issue_credential_request.set_request_uid(issue_request.request_uid)
    issue_credential_request.set_connection_id(issue_request.user_connection.connection_id)
    issue_credential_request.set_credential_values(issue_request.values_for_credential)

    credential_issue_invitation_response = dizme_agent_client.issue_credential_request(issue_credential_request)

    if credential_issue_invitation_response.status_code.is_failure():
        logger.error("Issue request not accepted error message: %s", credential_issue_invitation_response.message)
        raise IssueCredentialException(StatusCode.ERROR, MessagesCode.OPERATION_ERROR,
                                       DescriptionMessagesCodes.ERROR_DURING_ISSUE_CONTACT_SUPPORT)





