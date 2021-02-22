from generic_organization_service.entity import user_entity
from generic_organization_service.exception.operation_error import OperationError
from generic_organization_service.models import Organization, UserConnection
from generic_organization_service.utils.hash_service import encode
import logging

from django.db import transaction as django_transaction

logger = logging.getLogger(__name__)


def store_user(business_uid: str, organization: Organization) -> UserConnection:
    logger.info("confirm verify requested")
    created = True
    try:
        with django_transaction.atomic():

            hashed_username = encode(business_uid)

            user = user_entity.get_user_by_business_uid(business_uid)
            if user:
                user, created = user_entity.add_or_update_user(business_uid, hashed_username, hashed_username,
                                                               organization)
            else:
                user, created = user_entity.add_or_update_user(hashed_username, hashed_username, hashed_username,
                                                               organization)
            return user
    except OperationError as exc:
        logger.error("store access user error error %s ", str(exc))
        return None


def assign_user_connection(request_uid: str, connection_id: str, user: UserConnection) -> UserConnection:
    logger.info("assign_connection for request_uid: %s and connection_id: %s", request_uid, connection_id)
    try:
        user_connection = user_entity.update_user_connection(request_uid, connection_id, user=user)
        return user_connection
    except OperationError as exc:
        logger.error("store access user error error %s ", str(exc))
        return None
