from typing import Optional

from generic_organization_service.interfaces.responses.generic_response import GenericResponse,\
    MessagesCode, StatusCode


class CredentialIssueResponse(GenericResponse):
    def __init__(self, status_code: StatusCode, message_code: MessagesCode,
                 message: Optional[str] = None):
        super().__init__(status_code, message_code, message)
        self.response = None

    def set_response(self, ressponse: dict):
        self.response = ressponse

    def get_response(self) -> dict:
        return self.response
