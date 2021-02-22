from typing import Optional

from generic_organization_service.interfaces.responses.generic_response import GenericResponse, MessagesCode, \
    StatusCode


class ValueForCredentialResponse(GenericResponse):
    def __init__(self, status_code: StatusCode, message_code: MessagesCode,
                 message: Optional[str] = None):
        super().__init__(status_code, message_code, message)
        self.credential_def_id = None
        self.credential_values = None

    def set_credential_def_id(self, credential_def_id):
        self.credential_def_id = credential_def_id

    def get_credential_def_id(self):
        return self.credential_def_id

    def set_credential_values(self, credential_values: list):
        self.credential_values = credential_values

    def get_credential_values(self) -> list:
        return self.credential_values
