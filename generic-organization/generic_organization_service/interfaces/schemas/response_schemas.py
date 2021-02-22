from marshmallow import Schema, fields, post_dump, validates_schema, ValidationError


class GenericResponseSchema(Schema):
    class Meta:
        fields = ["status_code", "message_code", "message"]

    SKIP_VALUES = set([None])
    status_code = fields.Int(required=True, attribute="status_code")
    message_code = fields.Int(required=True, attribute="message_code")
    message = fields.Str(required=True, attribute="message")

    @post_dump
    def remove_skip_values(self, data):
        return {
            key: value for key, value in data.items()
            if type(value) is dict or type(value) is list or value not in self.SKIP_VALUES
        }


class ValuesForCredentialResponseSchema(GenericResponseSchema):
    class Meta:
        fields = GenericResponseSchema.Meta.fields + ["credential_name", "credential_values"]
    credential_name = fields.Str(attribute='credential_name', required=True)
    credential_values = fields.Dict(attribute='credential_values', required=True)


class DescriptionsSchema(Schema):
    lang = fields.Str(required=True, attribute="lang")
    message = fields.Str(required=True, attribute="message")


class ConfirmVerifyResponseSchema(GenericResponseSchema):
    class Meta:
        fields = GenericResponseSchema.Meta.fields + ["send_response", "result", "verify_result",
                                                      "descriptions"]

    result = fields.Bool(attribute='result', required=False)
    send_response = fields.Bool(attribute='send_response', required=True)
    descriptions = fields.Nested(DescriptionsSchema, many=True, attribute="descriptions",
                                 required=True, data_key="descriptions")
    verify_result = fields.Str(attribute='verify_result', default=None, required=False)


class VerifyRequestResponseSchema(GenericResponseSchema):
    class Meta:
        fields = GenericResponseSchema.Meta.fields + ["invitations"]

    invitations = fields.List(fields.Dict, required=False, attribute="invitations", many=True)


class ConnectionRequestResponseSchema(GenericResponseSchema):
    class Meta:
        fields = GenericResponseSchema.Meta.fields + ["invitations"]

    invitations = fields.List(fields.Dict, required=False, attribute="invitations", many=True)


