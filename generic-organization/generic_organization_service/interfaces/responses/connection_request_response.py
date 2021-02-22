from typing import Optional

from generic_organization_service.interfaces.responses.generic_response import GenericResponse, \
    MessagesCode, StatusCode


class ConnectionRequestResponse(GenericResponse):

    def __init__(self, status_code: StatusCode, message_code: MessagesCode,
                 message: Optional[str] = None):
        super().__init__(status_code, message_code, message)
        # Filled on response from organization
        self.invitations = None

    def set_invitations(self, invitations):
        self.invitations = invitations

    def get_invitations(self):
        return self.invitations
