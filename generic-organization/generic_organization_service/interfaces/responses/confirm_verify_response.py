from typing import Optional

from generic_organization_service.interfaces.responses.generic_response import GenericResponse, \
    MessagesCode, StatusCode, VerifyResult


class ConfirmVerifyResponse(GenericResponse):

    def __init__(self, status_code: StatusCode, message_code: MessagesCode,
                 message: Optional[str] = None):
        super().__init__(status_code, message_code, message)
        self.verify_result = VerifyResult.KO.value
        self.send_response = False
        self.descriptions = list()

    def set_verify_result(self, verify_result: VerifyResult):
        self.verify_result = verify_result.value

    def get_verify_result(self):
        return self.verify_result

    def set_send_response(self, send_response: bool):
        self.send_response = send_response

    def get_send_response(self) -> bool:
        return self.send_response

    def set_descriptions(self, descriptions: list):
        self.descriptions = descriptions

    def get_descriptions(self) -> list:
        return self.descriptions

