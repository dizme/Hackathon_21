from enum import Enum


class AttributeMimeType(Enum):
    TEXT_PLAIN_MIME_TYPE = "text/plain"
    IMAGE_JPG_MIME_TYPE = "image/jpg"


class CredentialValuesBuilder:
    def __init__(self):
        self.__credential_values = list()

    def add_attribute_values(self, name: str, value: str, mime_type: AttributeMimeType):
        attribute_value = dict()
        attribute_value["name"] = name
        attribute_value["value"] = value
        attribute_value["mime_type"] = mime_type.value
        self.__credential_values.append(attribute_value)
        return self

    def build(self) -> list:
        return self.__credential_values
