[Modernizing Applications with Apigee X](https://www.skills.google/paths/19/course_templates/714/labs/590371)


gcloud auth list
gcloud config list project

### Task 1. Deploy a backend service on Cloud Run

git clone --depth 1 https://github.com/GoogleCloudPlatform/training-data-analyst
ln -s ~/training-data-analyst/quests/develop-apis-apigee ~/develop-apis-apigee
cd ~/develop-apis-apigee/rest-backend
sed -i "s/us-west1/"REGION"/g" config.sh
-- Create Reasources -- Including Firestore in Native Mode --
cat init-project.sh
./init-project.sh
-->>> Check my Progress <<<------ 

Initialize the service ( creates a service account and adds two roles )
./init-service.sh

Deploy the backend service
./deploy.sh
-->>> Check my Progress <<<------ 

Test the service 
export RESTHOST=$(gcloud run services describe simplebank-rest --platform managed --region REGION --format 'value(status.url)')
echo "export RESTHOST=${RESTHOST}" >> ~/.bashrc

To verify that the service is running
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -X GET "${RESTHOST}/_status"

To verify that the service can write to Firestore

curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json" -X POST "${RESTHOST}/customers" -d '{"lastName": "Diallo", "firstName": "Temeka", "email": "temeka@example.com"}'

To verify that the service can read from Firestore,
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -X GET "${RESTHOST}/customers/temeka@example.com"

To load some additional sample data into Firestore
`gcloud firestore import gs://spls/shared/firestore-simplebank-data/firestore/example-data`

To retrieve the list of ATMs
`curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -X GET "${RESTHOST}/atms"`

To retrieve a single ATM
`curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -X GET "${RESTHOST}/atms/spruce-goose"`
( returns lat long )
In a later task, you will use Apigee and the Geocoding API to add an address to the response returned when retrieving a specific ATM.

### Task 2. Proxy the backend service with an Apigee API proxy