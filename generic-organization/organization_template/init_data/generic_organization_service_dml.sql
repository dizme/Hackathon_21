-- <<<<<   PAY ATTENTION   >>>>>
-- THIS IS ONLY AN EXAMPLE, PUT YOUR CONFIG PARAMETER AND STORE IN THE DB FOR YOUR ORGANIZATION

--INSERT INTO public.generic_organization_service_organization (id, name, business_code, ip_address) VALUES (1, 'Orgname','ORG_BC_001', 'http://xxxxx.yourendpoint.example');

--INSERT INTO public.generic_organization_service_agent (id, name, type, status, ip_address, auth, organization_id ) VALUES (1, 'DizmeAgent','AGENT', 'ACTIVE','https://demo-agent-cl.dizme.io','{"agent_id": "XXXXX", "token": "XXXX"}',1);

--INSERT INTO public.generic_organization_service_credential (id, name, business_code, version, attributes) VALUES (1, 'Email', 'Nkm6Gvyb5wCru52raJ8DkV:3:CL:80915:Email', '1.0', '["email", "timestamp"]');

--INSERT INTO public.generic_organization_service_action (id,name,description) VALUES (1, 'NO_ACTION', 'NO_ACTION');

--INSERT INTO public.generic_organization_service_service (id,name,description) VALUES (1, 'TEST','Verify for test');

--INSERT INTO public.generic_organization_service_proofrequest (id,business_code,version,description, organization_id) VALUES (1, 'PROOF_TEST_0000001', '1.0','Proof per TEST', 1);

--INSERT INTO public.generic_organization_service_proofserviceaction (id,action_id, proof_id, service_id) VALUES (1, 1,1,1);

--INSERT INTO public.generic_organization_service_proofserviceactioncredential (id, credential_id, proof_service_action_id) VALUES (1, 1,1);


