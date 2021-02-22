This folder is a template for organization APP. Copy this folder and rename with your organization name.

**In case you need to add some REST service, you have to put the definition path in the urls.py file present in your folder, the services will have the prefix /api/v1 by default**

The name of the folder cloned from "organization_template" must match (lower case) with the organization name inserted in the db in generic_organization_service_organization table 

In the apps.py present in your folder rename the field "name" and all reference **#your_org_name** with your organization folder name (lower case).

Adapt in the generic_organization_conf.env the environment variable with your environment reference.

You can use docker-compose-db-redis.yaml in order to start db and redis services needed to run your organization.

In the __init__py present in the root of your folder, set the default_app_config with the correct path to the class
present in the app.py file in your folder.

Implement the methods in your handler in order to receive callback from generic organization and develop your logic starting from 
the handler class "organization_handler.py" present in your folder

In case you need to add some textual descriptions, you can them in the localized files present in the resource/i18n folder.
If can add files for other language. 
The mapping with the key of the translation must be inserted in the organization_description_message_code.py class 

NOTE: The handler invocation is already made within properly redis worker so it not block the caller.

In case you need to make async a request received, you can use the method present in celery.async_event.delay(organization_name: str, event_type: str, request_data: dict), 
after that you'll receive callback on method handle_async_event of your handler. 

In order to correctly use your organization, you have to put some configuration within the DB. Look at the init_data folder,
there is a SQL file with an example of config. You have to customize the insert with your personal configuration.

The config to set are:

* Organization reference (Name and endpoint)
* Dizme Agent reference (configuration parameters of your dizme agent auth included)
* Credential (insert the credential reference you are enable to issue and put the credential_definition_id)
* Verify config
    * action => an action you can link to a proof & service 
    * service => a service you can link to a proof
    * proof request => the proof template reference configured on agent
    * proof_request_action => the link between proof, service and action.
    * proof_request_action_credential => if needed, the credential to issue for a proof & service & action
    
    
After configuration and startup, you can generate verify request in the following service:

* {running instance}/api/v1/organization/verification/start/<str:proof_business_code>/<str:service_name>
    * you'll obtain the verify link
* {running instance}/api/v1/organization/verification/start/<str:proof_business_code>/<str:service_name>/widget
    * the request will be started within the widget
    
In order to generate a connection request, you can use the following service:
* {running instance}/api/v1/organization/connection/start/<str:organization_business_code>
    * you'll obtain the invitation link