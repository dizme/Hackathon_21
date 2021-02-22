from generic_organization_service.handlers.organization_abstract_handler import OrganizationAbstractHandler
from antidote import register


@register(singleton=True)
class OrganizationHandlerManager:

    def __init__(self):
        self.handler_list = dict()

    def add_organization_handler(self, organization_name: str, handler: OrganizationAbstractHandler):
        self.handler_list[organization_name.lower()] = handler

    def get_organization_handler(self, organization_name: str) -> OrganizationAbstractHandler:
        return self.handler_list.get(organization_name.lower(), None)