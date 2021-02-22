from __future__ import absolute_import

import os, sys
import logging
from antidote import world

from celery import Celery
from celery import signals

sys.path.append(os.path.abspath('generic_organization'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'generic_organization.settings') # DON'T FORGET TO CHANGE THIS
import django
from django.conf import settings

django.setup()
import traceback
from generic_organization_service.utils.description_handler import DescriptionHandler, DescriptionMessagesCodes
from generic_organization_service.services.notification_service import NotificationService
from generic_organization_service.interfaces.responses.generic_response import VerifyResult
from generic_organization_service.handlers.organization_handler_manager import OrganizationHandlerManager, \
    OrganizationAbstractHandler
from generic_organization_service.entity import user_entity
app = Celery('generic_organization')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    task_routes = {
        'generic_organization.celery.*': {'queue': 'generic_organization'},
    },
)


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    return logging.getLogger('celery')


logger = logging.getLogger('celery')


@app.task(bind=True)
def handle_verify_confirm(self, organization_name: str, request_uid: str, connection_id: str,
                          presentation_id: str,  request_data: dict):
    logger.info("REDIS: handle_verify_confirm for request_uid: %s, connection_id: %s, presentation_id: %s ",
                request_uid, connection_id, presentation_id)
    try:
        description_handler = world.get(DescriptionHandler)
        notification_service = world.get(NotificationService)
        handler_manager: OrganizationHandlerManager = world.get(OrganizationHandlerManager)
        org_handler: OrganizationAbstractHandler = handler_manager.get_organization_handler(organization_name)
        # org_handler = VipMobileHandler()
        if org_handler:
            org_handler.handle_confirm_verify(request_uid, connection_id, presentation_id, request_data)
        return "OK"
    except Exception as ex:
        logger.error("Exception during handle_verify_confirm task: " + str(ex))
        if connection_id and presentation_id:
            user_connection = user_entity.get_user_connection(connection_id=connection_id)
            descriptions = description_handler.get_descriptions(DescriptionMessagesCodes.PROCESSING_ERROR)
            notification_service.send_verify_response(user_connection, presentation_id, descriptions, VerifyResult.KO)

        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return "An exception occurred"


@app.task(bind=True)
def handle_connection_notify(self, organization_name: str, request_uid: str, connection_id: str, request_data: dict):
    logger.info("REDIS: handle_connection_notify for request_uid: %s, connection_id: %s", request_uid, connection_id)
    try:
        handler_manager: OrganizationHandlerManager = world.get(OrganizationHandlerManager)
        org_handler: OrganizationAbstractHandler = handler_manager.get_organization_handler(organization_name)

        if org_handler:
            org_handler.handle_connection_notify(request_uid, connection_id, request_data)
        return "OK"
    except Exception as ex:
        logger.error("Exception during handle_connection_notify task: " + str(ex))
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return "An exception occurred"


@app.task(bind=True)
def handle_confirm_issue(self, organization_name: str, request_uid: str, connection_id: str, request_data: dict):
    logger.info("REDIS: handle_confirm_issue for request_uid: %s, connection_id: %s", request_uid, connection_id)
    try:
        handler_manager: OrganizationHandlerManager = world.get(OrganizationHandlerManager)
        org_handler: OrganizationAbstractHandler = handler_manager.get_organization_handler(organization_name)

        if org_handler:
            org_handler.handle_confirm_issue(request_uid, connection_id, request_data)
        return "OK"
    except Exception as ex:
        logger.error("Exception during handle_confirm_issue task: " + str(ex))
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return "An exception occurred"


@app.task(bind=True)
def handle_discard_credential(self, organization_name: str, request_uid: str, connection_id: str, request_data: dict):
    logger.info("REDIS: handle_discard_credential for request_uid: %s, connection_id: %s", request_uid, connection_id)
    try:
        handler_manager: OrganizationHandlerManager = world.get(OrganizationHandlerManager)
        org_handler: OrganizationAbstractHandler = handler_manager.get_organization_handler(organization_name)

        if org_handler:
            org_handler.handle_discard_credential(request_uid, connection_id, request_data)
        return "OK"
    except Exception as ex:
        logger.error("Exception during handle_confirm_issue task: " + str(ex))
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return "An exception occurred"


@app.task(bind=True)
def handle_discard_proof(self, organization_name: str, request_uid: str, connection_id: str, request_data: dict):
    logger.info("REDIS: handle_discard_proof for request_uid: %s, connection_id: %s", request_uid, connection_id)
    try:
        handler_manager: OrganizationHandlerManager = world.get(OrganizationHandlerManager)
        org_handler: OrganizationAbstractHandler = handler_manager.get_organization_handler(organization_name)

        if org_handler:
            org_handler.handle_discard_proof(request_uid, connection_id, request_data)
        return "OK"
    except Exception as ex:
        logger.error("Exception during handle_confirm_issue task: " + str(ex))
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return "An exception occurred"


@app.task(bind=True)
def async_event(self, organization_name: str, event_type: str, request_data: dict):
    logger.info("REDIS: async_event for organization_name: %s, event_type: %s", organization_name, event_type)
    try:
        handler_manager: OrganizationHandlerManager = world.get(OrganizationHandlerManager)
        org_handler: OrganizationAbstractHandler = handler_manager.get_organization_handler(organization_name)
        if org_handler:
            org_handler.handle_async_event(event_type, request_data)
        return "OK"
    except Exception as ex:
        logger.error("Exception during async_event task: " + str(ex))
        traceback.print_exception(type(ex), ex, ex.__traceback__)
        return "An exception occurred"
