from generic_organization_service.models import ProofServiceAction, Service, Action, ProofRequest, \
    ProofServiceActionCredential
from django.core.exceptions import ObjectDoesNotExist


def get_proof_service_actions(proof: ProofRequest = None, service: Service = None,
                              proof_name: str = None, service_name: str = None):
    try:
        filters = dict()

        if proof:
            filters['proof'] = proof
        if service:
            filters['service'] = service
        if proof_name:
            filters['proof__proof_name'] = proof_name
        if service_name:
            filters['service__service_name'] = service_name

        proof_service_actions = ProofServiceAction.objects.filter(**filters)
    except ObjectDoesNotExist:
        proof_service_actions = None
    return proof_service_actions


def get_proof_service_action(proof_business_code: str, service_name: str):
    try:
        filters = dict()

        filters['proof__business_code'] = proof_business_code
        filters['service__name'] = service_name

        proof_service_action = ProofServiceAction.objects.get(**filters)
    except ObjectDoesNotExist:
        proof_service_action = None
    return proof_service_action


def get_credentials_from_proof_service_action(proof_service_action: ProofServiceAction):
    try:
        filters = dict()
        filters['proof_service_action'] = proof_service_action
        credentials = ProofServiceActionCredential.objects.filter(**filters)
    except ObjectDoesNotExist:
        credentials = None
    return credentials
