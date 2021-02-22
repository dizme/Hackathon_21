from django.db import models
from django.utils import timezone
import pgcrypto

class Properties(models.Model):
    # name
    name = models.CharField(max_length=255, primary_key=True)
    # value
    value = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.value)


class Organization(models.Model):
    # name
    name = models.CharField(max_length=255, null=True)
    # business_code
    business_code = models.CharField(max_length=255, null=True)
    # address
    ip_address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{} - {}".format(self.name, self.ip_address)


class Agent(models.Model):
    # name
    name = models.CharField(max_length=255, null=True, unique=True)
    # type
    type = models.CharField(max_length=255, null=True)
    # status
    status = models.CharField(max_length=255, null=True)
    # address
    ip_address = models.CharField(max_length=255, null=True)
    # organization
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    # authentication
    auth = models.JSONField(null=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.id, self.name, self.type, self.status, self.ip_address)


class UserConnection(models.Model):
    connection_id = models.CharField(max_length=255, null=False)
    connection_date = models.DateTimeField(blank=True, default=timezone.now)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('connection_id', 'organization')

    def __str__(self):
        return "{} - {}".format(self.connection_id, self.organization)


class ConnectionAttribute(models.Model):
    name = models.CharField(max_length=255, null=False)
    value = models.TextField(null=False)
    user_connection = models.ForeignKey(UserConnection, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'value', 'user_connection')


class Request(models.Model):

    request_uid = models.CharField(max_length=255, null=False)

    start_date = models.DateTimeField(auto_now_add=True, blank=True)

    end_date = models.DateTimeField(blank=True, null=True)

    request_type = models.CharField(max_length=255, null=False)

    status = models.CharField(max_length=255, null=False)
    # organization
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    #user_connection
    user_connection = models.ForeignKey(UserConnection, on_delete=models.DO_NOTHING, null=True)
    # parent request
    parent_request = models.ForeignKey('self', default=None, on_delete=models.DO_NOTHING, null=True)


class Credential(models.Model):
    # name
    name = models.CharField(max_length=255, null=False)
    # business_code
    business_code = models.CharField(max_length=255, null=False)
    # version
    version = models.CharField(max_length=255, null=False)
    # value
    attributes = models.JSONField(null=False)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.name, self.business_code, self.version, self.value)


class IssueRequest(Request):

    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)

    values_for_credential = models.JSONField(null=True)

    discard_description = models.TextField(null=True)

    issued_by_operator = models.BooleanField(default=False)


class IssuedCredential(models.Model):
    request_uid = models.ForeignKey(Request, on_delete=models.CASCADE)

    tid = models.CharField(max_length=255, null=False)

    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)

    issue_date = models.DateTimeField(auto_now_add=True, blank=True)

    revoked_date = models.DateTimeField(blank=True, null=True)

    user_connection = models.ForeignKey(UserConnection, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.request_uid, self.credential, self.tid,
                                                    self.issue_date, self.revoked_date, self.user_connection)


class UserData(models.Model):
    user_connection = models.ForeignKey(UserConnection, on_delete=models.CASCADE)

    data = models.JSONField(null=False)

    source = models.CharField(max_length=255, null=False)

    request = models.ForeignKey(Request, on_delete=models.CASCADE)

    type = models.CharField(max_length=255, null=True)


class WebIdRequest(models.Model):
    request_uid = models.CharField(max_length=255, null=False)

    start_date = models.DateTimeField(auto_now_add=True, blank=True)

    end_date = models.DateTimeField(blank=True, null=True)

    request_type = models.CharField(max_length=255, null=False)

    status = models.CharField(max_length=255, null=False)

    dossier_id = models.CharField(max_length=255, null=False)

    verify_request_uid = models.CharField(max_length=255, null=True)

    presentation_id = models.CharField(max_length=255, null=False, default="N/A")


class WebIdDossier(models.Model):
    dossier_id = models.CharField(max_length=255, null=False)

    state = models.CharField(max_length=255, null=False)

    data = models.TextField(null=False)

    webid_request = models.ForeignKey(WebIdRequest, on_delete=models.DO_NOTHING)

    reason = models.CharField(max_length=255, null=True)

    user_connection = models.ForeignKey(UserConnection, on_delete=models.DO_NOTHING, null=True)

    token_link = models.CharField(max_length=255, null=True)

    creation_date = models.DateTimeField(auto_now_add=True, blank=True)

    last_update_date = models.DateTimeField(blank=True)


class WebIdUserData(UserData):
    webid_request = models.ForeignKey(WebIdRequest, on_delete=models.CASCADE)


class IqpRequest(models.Model):
    request_uid = models.CharField(max_length=255, null=False)

    start_date = models.DateTimeField(auto_now_add=True, blank=True)

    end_date = models.DateTimeField(blank=True, null=True)

    status = models.CharField(max_length=255, null=False)

    dossier_id = models.CharField(max_length=255, null=False)

    process_id = models.CharField(max_length=255, null=False)

    verify_request_uid = models.CharField(max_length=255, null=True)

    presentation_id = models.CharField(max_length=255, null=False, default="N/A")


class IqpDossier(models.Model):
    dossier_id = models.CharField(max_length=255, null=False)

    state = models.CharField(max_length=255, null=False)

    data = models.TextField(null=False)

    iqp_request = models.ForeignKey(IqpRequest, on_delete=models.DO_NOTHING)

    reason = models.CharField(max_length=255, null=True)

    awaited_owner_confirmation = models.IntegerField(null=True, default=0)

    user_connection = models.ForeignKey(UserConnection, on_delete=models.DO_NOTHING, null=True)

    creation_date = models.DateTimeField(auto_now_add=True, blank=True)

    last_update_date = models.DateTimeField(blank=True)


class IqpUserData(UserData):
    iqp_request = models.ForeignKey(IqpRequest, on_delete=models.CASCADE)


class ProofRequest(models.Model):
    # name
    business_code = models.CharField(max_length=255, null=False)
    # version
    version = models.CharField(max_length=255, null=False)
    # description
    description = models.CharField(max_length=255, null=False)
    # organization
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} - {} - {}".format(self.id, self.business_code, self.version, self.description)


class Service(models.Model):
    # related string
    name = models.CharField(max_length=255, null=False)
    # description
    description = models.CharField(max_length=255, null=False, unique=True)


class Action(models.Model):
    name = models.CharField(max_length=255, null=False)

    description = models.CharField(max_length=255, null=False)


class ProofServiceAction(models.Model):

    proof = models.ForeignKey(ProofRequest, on_delete=models.CASCADE)

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    action = models.ForeignKey(Action, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('proof', 'service')


class ProofServiceActionCredential(models.Model):

    proof_service_action = models.ForeignKey(ProofServiceAction, on_delete=models.CASCADE)

    credential = models.ForeignKey(Credential, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('proof_service_action', 'credential')


class VerifyRequest(Request):

    proof_service_action = models.ForeignKey(ProofServiceAction, on_delete=models.CASCADE)

    allow_multiple_read = models.BooleanField(default=False, null=False)

    restrictions = models.TextField(null=True)


class ConnectionRequest(Request):
    allow_multiple_read = models.BooleanField(default=False, null=False)


class VerifyConfirm(models.Model):

    verify_request = models.ForeignKey(VerifyRequest, on_delete=models.CASCADE)

    confirm_date = models.DateTimeField(null=True)

    proof_evidence = pgcrypto.EncryptedTextField(null=False)

    proof_request = models.JSONField(null=True)

    user_connection = models.ForeignKey(UserConnection, on_delete=models.DO_NOTHING, null=True)

    status = models.CharField(max_length=255, null=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.verify_request, self.confirm_date, self.proof_evidence,
                                          self.proof_request, self.user_connection)
