Task 1. Proxy the backend service with an Apigee API proxy

export SERVICE_URL=$(gcloud run services describe simplebank-rest --platform managed --region us-east1 --format 'value(status.url)')
SERVICE_URL=https://simplebank-rest-odrgw25npa-ue.a.run.app

Proxy Development -> Api Proxies -> + Create
- Create a Reverse Proxy
- Proxy Name: bank-v1
- Base Path: /bank/v1
- Target (Existing API): https://simplebank-rest-odrgw25npa-ue.a.run.app
- next -> Create


Task 2. Add a VerifyAPIKey policy
- Develop
- Proxy Endpoints -> default -> Request -> PreFlow + Add Policy Step
  ( keys should be placed early in the process )
- Create New Policy
- Select -> Security -> VerifyAPIKey
  - VA-VerifyKey
  - VA-VerifyKey
  - no condition

select the VA-VerifyKey ( modify xml)
In the APIKey element, replace request.queryparam.apikey with request.header.apikey

An API key is less likely to be logged or saved in browser history if it is specified in a header.

Modify the target to send an OpenID Connect identity token

Click: Target Endpoints -> default -> PreFlow
look at the xml
in <HTTPTargetConnection>
below <URL>
add
        <Authentication>
            <GoogleIDToken>
                <Audience>AUDIENCE</Audience>
            </GoogleIDToken>
        </Authentication>

replace AUDIENCE -> https://simplebank-rest-odrgw25npa-ue.a.run.app

Save

Confirm the runtime instance is avaliable
```
export INSTANCE_NAME=eval-instance; export ENV_NAME=eval; export PREV_INSTANCE_STATE=; echo "waiting for runtime instance ${INSTANCE_NAME} to be active"; while : ; do export INSTANCE_STATE=$(curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" -X GET "https://apigee.googleapis.com/v1/organizations/${GOOGLE_CLOUD_PROJECT}/instances/${INSTANCE_NAME}" | jq "select(.state != null) | .state" --raw-output); [[ "${INSTANCE_STATE}" == "${PREV_INSTANCE_STATE}" ]] || (echo; echo "INSTANCE_STATE=${INSTANCE_STATE}"); export PREV_INSTANCE_STATE=${INSTANCE_STATE}; [[ "${INSTANCE_STATE}" != "ACTIVE" ]] || break; echo -n "."; sleep 5; done; echo; echo "instance created, waiting for environment ${ENV_NAME} to be attached to instance"; while : ; do export ATTACHMENT_DONE=$(curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" -X GET "https://apigee.googleapis.com/v1/organizations/${GOOGLE_CLOUD_PROJECT}/instances/${INSTANCE_NAME}/attachments" | jq "select(.attachments != null) | .attachments[] | select(.environment == \"${ENV_NAME}\") | .environment" --join-output); [[ "${ATTACHMENT_DONE}" != "${ENV_NAME}" ]] || break; echo -n "."; sleep 5; done; echo "***ORG IS READY TO USE***";
```

Deploy the API proxy
Deploy 
Service Account: apigee-internal-access@qwiklabs-gcp-02-476aa60ad576.iam.gserviceaccount.com


Test the API proxy
ssh to machine on the internal network

TEST_VM_ZONE=$(gcloud compute instances list --filter="name=('apigeex-test-vm')" --format "value(zone)")
gcloud compute ssh apigeex-test-vm --zone=${TEST_VM_ZONE} --force-key-file-overwrite

curl -i -k -X GET "https://eval.example.com/bank/v1/customers"

got 401 ( which is what we wanted, no API key was provided )

Task 3. Add API products and an application
(You can think of API products as your product line.)
You will then create two applications and associate separate API products for them, providing them with different access.
Create the first API product
- Distribution > API Products -> + Create
(TODO: add the details for creating bank-fullaccess and bank-readonly here)

Create an app developer
Distribution > Developers -> + Create

Create an app with read-only access
Distrobution > Apps -> + Create
( TODO: more notes here )
Create an app with full access

Test the api key w/ ssh
TEST_VM_ZONE=$(gcloud compute instances list --filter="name=('apigeex-test-vm')" --format "value(zone)")
gcloud compute ssh apigeex-test-vm --zone=${TEST_VM_ZONE} --force-key-file-overwrite

To get the API key for the read-only application
export PROJECT_ID=$(gcloud config list --format 'value(core.project)' 2>/dev/null)
echo "PROJECT_ID=${PROJECT_ID}"
export API_KEY=$(curl -s -H "Authorization: Bearer $(gcloud auth print-access-token)" -X GET "https://apigee.googleapis.com/v1/organizations/${PROJECT_ID}/developers/joe@example.com/apps/readonly-app" | jq ".credentials[0].consumerKey" --raw-output)
echo "API_KEY=${API_KEY}"

Call the deployed bank-v1 API proxy in the eval environment, using a fake API key:
curl -i -k -X GET -H "apikey: ABC123" "https://eval.example.com/bank/v1/customers"
{"errorcode":"oauth.v2.InvalidApiKey"}

Call the deployed bank-v1 API proxy in the eval environment, using the real API key:
curl -i -k -X GET -H "apikey: ${API_KEY}" "https://eval.example.com/bank/v1/customers"
another request
curl -i -k -X POST -H "apikey: ${API_KEY}" -H "Content-Type: application/json" "https://eval.example.com/bank/v1/customers" -d '{"firstName": "Julia", "lastName": "Dancey", "email": "julia@example.org"}'

detail":{"errorcode":"oauth.v2.InvalidApiKeyForGivenResource"}

Task 4. Enforce a quota

Task 5. Add CORS to the API proxy

Task 6. Download and modify an OpenAPI specification