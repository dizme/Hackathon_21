from marshmallow import (Schema, fields, validates_schema, ValidationError)


class DescriptionsSchema(Schema):
    lang = fields.Str(required=True, attribute="lang")
    message = fields.Str(required=True, attribute="message")


class ValuesForCredentialRequestSchema(Schema):
    connection_id = fields.Str(attribute="connection_id", required=True)
    credential_def_id = fields.Str(attribute="credential_def_id", required=True)
    request_uid = fields.Str(attribute="request_uid", required=True)
    parent_request_uid = fields.Str(attribute="parent_request_uid", required=False)


class ConfirmIssueRequestSchema(Schema):
    connection_id = fields.Str(attribute="connection_id", required=True)
    request_uid = fields.Str(attribute="request_uid", required=True)
    credential_def_id = fields.Str(attribute="credential_def_id", required=True)
    tid = fields.Str(attribute="tid", required=True)
    credential_revocation_id = fields.Str(attribute="credential_revocation_id", required=False)


class DiscardCredentialRequestSchema(Schema):
    connection_id = fields.Str(attribute="connection_id", required=True)
    request_uid = fields.Str(attribute="request_uid", required=True, allow_none=False)
    credential_def_id = fields.Str(attribute="credential_def_id", required=True)
    description = fields.Str(attribute="description", required=True)
    data_not_valid = fields.Bool(attribute="data_not_valid", required=True)


class DiscardProofRequestSchema(Schema):
    connection_id = fields.Str(attribute="connection_id", required=True)
    request_uid = fields.Str(attribute="request_uid", required=True, allow_none=False)
    description = fields.Str(attribute="description", required=True)


class ConnectionNotifyRequestSchema(Schema):
    connection_id = fields.Str(attribute="connection_id", required=True)
    status = fields.Str(attribute="status", required=True)
    request_uid = fields.Str(attribute="request_uid", required=True)
    reused = fields.Bool(attribute="reused", required=True)


class ConfirmIdentificationSchema(Schema):
    business_id = fields.Str(attribute="business_id", load_from="businessId", allow_none=True, required=False)
    status = fields.Str(attribute="status", load_from="status", required=True)
    creation_date = fields.Int(attribute="creation_date", load_from="creationDate", required=True)
    last_activity_date = fields.Int(attribute="last_activity_date", load_from="lastActivityDate", required=True)


class ConfirmIqpSchema(Schema):
    dossier_id = fields.Str(attribute="dossier_id", load_from="dossierId", required=True)
    status = fields.Str(attribute="status", load_from="status", required=True)
    reject_reason = fields.Str(attribute="reject_reason", load_from="rejectReason", required=False)


class ConfirmIqpScoresSchema(Schema):
    process_instance_id = fields.Str(attribute="process_instance_id", load_from="processInstanceId", required=True)
    process_id = fields.Str(attribute="process_id", load_from="processId", required=True)
    dossier_id = fields.Str(attribute="dossier_id", load_from="dossierId", required=True)
    step = fields.Str(attribute="step", load_from="step", required=True)
    status = fields.Str(attribute="status", load_from="status", required=True)


class StartVerifyRequestSchema(Schema):
    proof_business_code = fields.Str(attribute="proof_business_code", required=True)
    service = fields.Str(attribute="service", required=True)
    restrictions = fields.Dict(attribute="restrictions", required=False)
    allow_multiple_read = fields.Bool(attribute="allow_multiple_read", required=False)


class StartConnectionRequestSchema(Schema):
    organization_business_code = fields.Str(required=True, attribute="organization_business_code")
    allow_multiple_read = fields.Bool(attribute="allow_multiple_read", required=False)


class ConfirmVerifyRequestSchema(Schema):
    request_uid = fields.Str(attribute="request_uid", required=True)
    organization_name = fields.Str(required=True, attribute="organization_name")
    proof_business_code = fields.Str(required=True, attribute="proof_business_code")
    revealed_attributes = fields.Dict(attribute="revealed_attributes", required=True)
    unrevealed_attributes = fields.Dict(attribute="unrevealed_attributes", required=True)
    self_attested_attributes = fields.Dict(attribute="self_attested_attributes", required=True)
    proof = fields.Dict(attribute="proof", required=True)
    proof_request = fields.Dict(attribute="proof_request", required=True)
    presentation_id = fields.Str(attribute="presentation_id", required=True)
    connection_id = fields.Str(attribute="connection_id", required=True)