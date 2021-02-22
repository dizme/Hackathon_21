from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import start_verify, start_verify_with_widget, confirm_verify, connection_notify, confirm_issue, \
    discard_credential, discard_proof, values_for_credential, start_connection


urlpatterns = [
    path('organization/verification/start/<str:proof_business_code>/<str:service_name>', start_verify,
         name="start_verify"),
    path('organization/verification/start/<str:proof_business_code>/<str:service_name>/widget',
         start_verify_with_widget, name="start_verify_with_widget"),

    path('organization/connection/start/<str:organization_business_code>', start_connection,
         name="start_verify"),

    path('verification/verify/confirm', confirm_verify, name="confirm_verify"),
    path('owners/connection/notify', connection_notify, name="connection_notify"),
    path('owners/credential/confirm_issue', confirm_issue, name="confirm_issue"),
    path('owners/credential/discard', discard_credential, name="discard_credential"),
    path('owners/proof/discard', discard_proof, name="discard_proof"),
    path('owners/credential/values_for_credential', values_for_credential, name="values_for_credential"),

]

urlpatterns = format_suffix_patterns(urlpatterns)