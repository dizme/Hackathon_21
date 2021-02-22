from typing import Optional
from enum import IntEnum, Enum


class Description:
    def __init__(self, lang, message):
        self.lang = lang
        self.message = message

    def __str__(self):
        return "Lang: {} - Message: {}".format(self.lang, self.message)


class DescriptionBuilder:
    def __init__(self):
        self.descriptions = list()

    def add_description(self, lang, message):
        self.descriptions.append(Description(lang, message))
        return self

    def build(self):
        return self.descriptions


class StatusCode(IntEnum):
    SUCCESS = 100,
    ERROR = 101,

    def is_success(self):
        return self is StatusCode.SUCCESS

    def is_failure(self):
        return not self.is_success()


class MessagesCode(IntEnum):
    SUCCESS = 0,
    OPERATION_ERROR = 1


class VerifyResult(Enum):
    OK = 'OK'
    KO = 'KO'
    IN_PROGRESS = 'IN_PROGRESS'

    @staticmethod
    def from_value(value):
        if not value:
            return None
        for c in VerifyResult:
            if c.value == value:
                return c
        return None


class GenericResponse:

    def __init__(self, status_code: StatusCode, message_code: MessagesCode,
                 message: Optional[str] = None):
        self.status_code = status_code
        self.message_code = message_code
        self.message = message

    def __str__(self):
        return "Status code: {} - Message: {} - Message Code; {}".format(self.status_code, self.message)
