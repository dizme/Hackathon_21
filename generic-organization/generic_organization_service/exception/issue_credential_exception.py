from generic_organization_service.interfaces.responses.generic_response import MessagesCode, StatusCode
from generic_organization_service.utils.description_handler import DescriptionMessagesCodes, DescriptionHandler
from antidote import world


class IssueCredentialException(BaseException):

    def __init__(self, status_code: StatusCode, message_code: MessagesCode,
                 description_code: DescriptionMessagesCodes = DescriptionMessagesCodes.UNDEFINED):
        self.description_handler = world.get(DescriptionHandler)
        self.status_code = status_code
        self.message_code = message_code
        self.description_code = description_code

    def get_status_code(self):
        return self.status_code

    def get_message_code(self):
        return self.message_code

    def get_descriptions(self):
        return self.description_handler.get_descriptions(self.description_code)

    def get_description_code(self):
        return self.description_code.value

