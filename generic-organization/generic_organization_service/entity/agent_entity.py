from generic_organization_service.models import Agent, Organization
from django.core.exceptions import ObjectDoesNotExist
from enum import Enum


class AgentStatus(Enum):
    ACTIVE = 'ACTIVE'
    DISABLED = 'DISABLED'

    def __str__(self):
        return self.value


class AgentAuthHeader(Enum):
    ORGANIZATION_AGENT_ID = "agent_id"
    ORGANIZATION_AGENT_TOKEN = "token"


def get_active_agent(organization: Organization = None) -> Agent:
    agent = get_agent(status=AgentStatus.ACTIVE, organization=organization)
    if agent:
        return agent[0]
    return None


def get_agent(status: AgentStatus = AgentStatus.ACTIVE, agent_id=None,
              name=None, organization: Organization = None):
    try:
        filters = dict()

        if status:
            filters['status'] = status.value
        if agent_id:
            filters['id'] = agent_id
        if name:
            filters['name'] = name
        if organization:
            filters['organization'] = organization

        agent = Agent.objects.filter(**filters)
    except ObjectDoesNotExist:
        agent = None
    return agent
