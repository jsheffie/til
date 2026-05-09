## Labs Completed
| Completed | Title | Location | 
|--------|--------|---|
| 11/02/2025 | [5 Develop Serverless Applications on Cloud Run: Challenge Lab](https://www.skills.google/paths/19/course_templates/741/labs/592448) | PCDP -> 11 Develop Serverless Applications on Cloud Run |


Deploy Staging Architecture
Deploy Prod Architecture
Secure Access Between the components in the Prod Architecuture

```sh
gcloud auth list
gcloud config list project

gcloud config set project \
$(gcloud projects list --format='value(PROJECT_ID)' \
--filter='qwiklabs-gcp')

export PROJECT_ID=$(gcloud projects list --format='value(PROJECT_ID)' \
--filter='qwiklabs-gcp')

export REGION=us-central1
gcloud config set run/region ${REGION}
gcloud config set run/platform managed

gcloud config list project

git clone https://github.com/rosera/pet-theory.git && cd pet-theory/lab07
```

```sh
gcloud services list
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

```sh
# Do we have an artifact registory already?
# gcloud artifacts repositories create pet-theory-repo --repository-format=docker --location=${REGION} --description="My Docker repo
```

### Task 1. Enable a public service
```sh
cd ~/pet-theory/lab07/unit-api-billing
# npm install express
gcloud builds submit --tag gcr.io/${PROJECT_ID}/billing-staging-api:0.1
# gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/pet-theory-repo/billing-staging-api:0.1 .

#   --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-repo/billing-staging-api:0.1 \
gcloud run deploy public-billing-service-650 \
  --image gcr.io/${PROJECT_ID}/billing-staging-api:0.1 \
  --platform managed \
  --region ${REGION}
  --allow-unauthenticated
  --max-instances=1


# gcloud run services describe public-billing-service --region ${REGION}
export BILLING_URL=$(gcloud beta run services describe public-billing-service-650 --platform managed --region ${REGION} --format="value(status.url)")
curl -X get $BILLING_URL
```


### Task 2. Deploy a frontend service
```sh
cd ~/pet-theory/lab07/staging-frontend-billing
npm install express hbs google-auth-library node-fetch got

# modify the app.js file
# const REST_API_SERVICE = new URL("https://billing-service-st43nxgwmq-uc.a.run.app" + "/billing");
const REST_API_SERVICE = new URL(process.env.SERVICE_URL + "/billing");

gcloud builds submit --tag gcr.io/${PROJECT_ID}/frontend-staging:0.1

gcloud run deploy frontend-staging-service-792 \
  --image gcr.io/${PROJECT_ID}/frontend-staging:0.1 \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --max-instances=1 \
  --set-env-vars SERVICE_URL=${BILLING_URL}

export FRONTEND_URL=$(gcloud beta run services describe frontend-staging-service-792 --platform managed --region ${REGION} --format="value(status.url)")
curl -X get $FRONTEND_URL

```

### Task 3. Deploy a private service

```sh
gcloud run services delete private-billing-service-650 --region ${REGION}
gcloud run services delete frontend-staging-service-792 --region ${REGION}
```

```sh
cd ~/pet-theory/lab07/staging-api-billing
gcloud builds submit --tag gcr.io/${PROJECT_ID}/billing-staging-api:0.2

gcloud run deploy private-billing-service-822 \
  --image gcr.io/${PROJECT_ID}/billing-staging-api:0.2 \
  --platform managed \
  --region ${REGION}
  --no-unauthenticated
  --max-instances=1

export BILLING_URL=$(gcloud beta run services describe private-billing-service-822 --platform managed --region ${REGION} --format="value(status.url)")
curl -X get -H "Authorization: Bearer $(gcloud auth print-identity-token)" $BILLING_URL
export SERVICE_URL=$(gcloud beta run services describe private-billing-service-822 --platform managed --region ${REGION} --format="value(status.url)")
```

### Task 4. Create a billing service account
create service account
```sh
gcloud iam service-accounts create billing-service-sa-960 --display-name "Billing Service Cloud Run"
```

### Task 5. Deploy the billing service

```sh
cd ~/pet-theory/lab07/prod-api-billing
gcloud builds submit --tag gcr.io/${PROJECT_ID}/billing-prod-api:0.1

gcloud run deploy billing-prod-service-809 \
  --image gcr.io/${PROJECT_ID}/billing-prod-api:0.1 \
  --platform managed \
  --region ${REGION} \
  --max-instances=1

## WTF: enable the service account mean?
gcloud beta run services add-iam-policy-binding billing-prod-service-809 --member=serviceAccount:billing-service-sa-960@${PROJECT_ID}.iam.gserviceaccount.com --role=roles/run.invoker --platform managed --region ${REGION}

# gcloud projects list
# export PROJECT_NUMBER=940356350225

# Then enable your project to create Cloud ~~Pub/Sub~~ authentication tokens:
# gcloud projects add-iam-policy-binding ${PROJECT_ID} --member=serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-pubsub.iam.gserviceaccount.com --role=roles/iam.serviceAccountTokenCreator

export PROD_BILLING_URL=$(gcloud run services describe private-billing-service-822 \
--platform managed \
--region ${REGION} \
--format "value(status.url)")

curl -X get -H "Authorization: Bearer \
$(gcloud auth print-identity-token)" \
$PROD_BILLING_URL

```

### Task 6. Frontend service account

create service account
```sh
gcloud iam service-accounts create frontend-service-sa-161 --display-name "Billing Service Cloud Run Invoker"
```
service accout perms ( iam policy binding frontend-prod-service <-> service account <-> role)

```sh

gcloud beta run services add-iam-policy-binding frontend-staging-service-792 --member=serviceAccount:frontend-service-sa-161@${PROJECT_ID}.iam.gserviceaccount.com --role=roles/run.invoker --platform managed --region ${REGION}


# gcloud beta run services add-iam-policy-binding frontend-prod-service --member=serviceAccount:frontend-service-sa-161@${PROJECT_ID}.iam.gserviceaccount.com --role=roles/run.invoker --platform managed --region ${REGION}
```

### Task 7. Redeploy the frontend service

```sh
cd ~/pet-theory/lab07/prod-frontend-billing
npm install express hbs google-auth-library node-fetch got

# modify the app.js file
# const REST_API_SERVICE = new URL("https://billing-service-st43nxgwmq-uc.a.run.app" + "/billing");
const REST_API_SERVICE = new URL(process.env.SERVICE_URL + "/billing");

gcloud builds submit --tag gcr.io/${PROJECT_ID}/frontend-prod:0.1

gcloud run deploy frontend-prod-service-543 \
  --image gcr.io/${PROJECT_ID}/frontend-prod:0.1 \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --max-instances=1 \
  --service-account=frontend-service-sa-161@${PROJECT_ID}.iam.gserviceaccount.com \
  --set-env-vars BILLING_URL=${PROD_BILLING_URL}

export FRONTEND_URL=$(gcloud beta run services describe frontend-prod-service-543 --platform managed --region ${REGION} --format="value(status.url)")
curl -X get $FRONTEND_URL





### Debugging
```sh
gcloud builds list
gcloud artifacts docker images list ${REGION}-docker.pkg.dev/${PROJECT_ID}/pet-theory-repo
```
