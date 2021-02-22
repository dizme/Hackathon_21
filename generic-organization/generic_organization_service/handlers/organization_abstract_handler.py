from abc import ABC, abstractmethod


class OrganizationAbstractHandler(ABC):

    @abstractmethod
    def handle_confirm_verify(self, request_uid: str, connection_id: str, presentation_id, request_data: dict()):
        pass

    @abstractmethod
    def handle_connection_notify(self, request_uid: str, connection_id: str, request_data: dict()):
        pass

    @abstractmethod
    def handle_confirm_issue(self, request_uid: str, connection_id: str, request_data: dict()):
        pass

    @abstractmethod
    def handle_discard_credential(self, request_uid: str, connection_id: str, request_data: dict()):
        pass

    @abstractmethod
    def handle_discard_proof(self, request_uid: str, connection_id: str, request_data: dict()):
        pass

    @abstractmethod
    def handle_values_for_credential(self, request_uid: str, connection_id: str, request_data: dict()) -> list:
        pass

    @abstractmethod
    def handle_async_event(self,event_type: str, request_data: dict):
        pass