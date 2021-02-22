import logging

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from antidote import inject

from generic_organization_service.services.verify_service import VerifyService
from generic_organization_service.services.connection_service import ConnectionService
from generic_organization_service.services.issue_service import IssueService

logger = logging.getLogger(__name__)


@csrf_exempt
@api_view(["GET"])
@permission_classes(())
@inject
def start_verify(request, proof_business_code, service_name, verify_service: VerifyService, *args, **kwargs):
    logger.info("start_verify for business_code: %s and service_name: %s", proof_business_code, service_name)
    allow_multiple_read = request.GET.get("allow_multiple_read", "false")

    request.data['proof_business_code'] = proof_business_code
    request.data['service'] = service_name
    request.data['restrictions'] = {}
    request.data['allow_multiple_read'] = True if (allow_multiple_read == "True" or allow_multiple_read == "true") \
        else False
    return verify_service.start_verify(request.data)

@csrf_exempt
@api_view(["GET"])
@permission_classes(())
@inject
def start_connection(request, organization_business_code, connection_service: ConnectionService, *args, **kwargs):
    logger.info("start_connection for organization_business_code: %s", organization_business_code)
    allow_multiple_read = request.GET.get("allow_multiple_read", "false")
    request.data['organization_business_code'] = organization_business_code
    request.data['allow_multiple_read'] = True if (allow_multiple_read == "True" or allow_multiple_read == "true") \
        else False
    return connection_service.start_connection(request.data)


@csrf_exempt
@api_view(["GET"])
@permission_classes(())
@inject
def start_verify_with_widget(request, proof_business_code, service_name, verify_service: VerifyService, *args, **kwargs):
    logger.info("start_verify for business_code: %s and service_name: %s", proof_business_code, service_name)
    allow_multiple_read = request.GET.get("allow_multiple_read", "false")

    request.data['proof_business_code'] = proof_business_code
    request.data['service'] = service_name
    request.data['restrictions'] = {}
    request.data['allow_multiple_read'] = True if (allow_multiple_read == "True" or allow_multiple_read == "true") \
        else False
    return verify_service.start_verify_with_widget(request.data)


@csrf_exempt
@api_view(["POST"])
@inject
@permission_classes(())
def confirm_verify(request, verify_service: VerifyService, *args, **kwargs):
    logger.info("confirm_verify")
    return verify_service.confirm_verify(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def connection_notify(request, connection_service: ConnectionService, *args, **kwargs):
    logger.info("connection_notify")
    return connection_service.connection_notify(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def confirm_issue(request, issue_service: IssueService, *args, **kwargs):
    logger.info("confirm_issue")
    return issue_service.confirm_issue(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def discard_credential(request, issue_service: IssueService, *args, **kwargs):
    logger.info("discard_credential")
    return issue_service.discard_credential(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def discard_proof(request, verify_service: VerifyService, *args, **kwargs):
    logger.info("discard_credential")
    return verify_service.discard_proof(request.data)


@csrf_exempt
@api_view(["POST"])
@permission_classes(())
@inject
def values_for_credential(request, issue_service: IssueService, *args, **kwargs):
    logger.info("discard_credential")
    return issue_service.values_for_credential(request.data)
