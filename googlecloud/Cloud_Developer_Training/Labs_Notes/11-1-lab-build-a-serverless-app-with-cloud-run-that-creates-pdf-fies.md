## Labs Completed
| Completed | Title | Location | 
|--------|--------|---|
| 11/02/2025 | [Build a Serverless App with Cloud Run that Creates PDF Files](https://www.skills.google/paths/19/course_templates/741/labs/592444) | PCDP -> 11 Develop Serverless Applications on Cloud Run |


<details><summary>Activate Cloud Shell</summary>

```sh
gcloud cheat-sheet
gcloud auth list
gcloud config list project

Additional Notes:
gcloud config set account jeff.sheffield@gmail.com
gcloud confg set project PROJECT_ID
gcloud auth application-default login
```
</details>

<details><summary>Task 1. Understanding the task</summary>

It looks like we can run LibreOffice in a serverless environment with Cloud Run. No server maintenance is needed!
</details>

<details><summary>Task 2. Enable the Cloud Run API</summary>

```sh
gcloud services list
gcloud services enable run.googleapis.com
```
</details>

<details><summary>Task 3. Deploy a simple Cloud Run service: pet-theory</summary>

- build it ( gcloud builds submit )
- deploy it ( gcloud run deploy )
   - get service url ( gcloud beta run services describe )
   - curl -X POST $SERVICE_URL ( fails )
   - curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" $SERVICE_URL

```sh
git clone https://github.com/rosera/pet-theory.git
cd pet-theory/lab03
```
edit `package.json`
```
...

"scripts": {
    "start": "node index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },

...
```
Install remaining components w/ node js
```sh
npm install express
npm install body-parser
npm install child_process
npm install @google-cloud/storage
```
Review
- `lab03/index.js`
- `lab03/Dockerfile`

### Build it (gcloud builds submit)
```sh
export PROJECT_ID=qwiklabs-gcp-01-78e2c76d3e33
gcloud builds submit --tag gcr.io/${PROJECT_ID}/pdf-converter
```

### Deploy it (gcloud run deploy)to the Artifacts Registry
```sh
export REGION=us-west1
gcloud run deploy pdf-converter \
  --image gcr.io/${PROJECT_ID}/pdf-converter \
  --platform managed \
  --region ${REGION} \
  --no-allow-unauthenticated \
  --max-instances=1
```

Create the environment variable $SERVICE_URL for the app so you can easily access it
```sh
export SERVICE_URL=$(gcloud beta run services describe pdf-converter --platform managed --region ${REGION} --format="value(status.url)")
echo $SERVICE_URL
```

```sh
curl -X POST $SERVICE_URL
```
"Your client does not have permission to get the URL"

```sh
curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" $SERVICE_URL
```
</details>



<details><summary>Task 4. Trigger your Cloud Run service when a new file is uploaded (setup pub/sub)</summary>

- create the buckets 
- create Pub/Sub notification (gsutil notification create)
- create service account ( cloud storage -> cloud run )
- modify the service account permissions ( iam policy binding run-service <-> service account <-> role)
- policy binding: use (unique) PROJECT_NUMBER to modify service account to eble your project to create Cloud Pub/Sub authentication tokens
    - gcloud projects add-iam-policy-binding ( project <-> service account <-> role serviceAccountTokenCreator
    )
- Finally, create a Pub/Sub subscription so that the PDF converter can run whenever a message is published on the topic "new-doc".
 

```sh
gsutil mb gs://${PROJECT_ID}-upload
gsutil mb gs://${PROJECT_ID}-processed
```

create the notification on topic `new-doc`
```sh
gsutil notification create -t new-doc -f json -e OBJECT_FINALIZE gs://${PROJECT_ID}-upload
```

create service account
```sh
gcloud iam service-accounts create pubsub-cloud-run-invoker --display-name "PubSub Cloud Run Invoker"
```
service accout perms ( iam policy binding run-service <-> service account <-> role)

```sh
gcloud beta run services add-iam-policy-binding pdf-converter --member=serviceAccount:pubsub-cloud-run-invoker@${PROJECT_ID}.iam.gserviceaccount.com --role=roles/run.invoker --platform managed --region ${REGION}
```

```sh
gcloud projects list
export PROJECT_NUMBER=562124204647
```
Then enable your project to create Cloud Pub/Sub authentication tokens:

```sh
gcloud projects add-iam-policy-binding ${PROJECT_ID} --member=serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-pubsub.iam.gserviceaccount.com --role=roles/iam.serviceAccountTokenCreator
```

Finally, create a Pub/Sub subscription so that the PDF converter can run whenever a message is published on the topic "new-doc".
```sh
gcloud beta pubsub subscriptions create pdf-conv-sub --topic new-doc --push-endpoint=$SERVICE_URL --push-auth-service-account=pubsub-cloud-run-invoker@${PROJECT_ID}.iam.gserviceaccount.com
```

</details>


<details><summary>Task 5. See if the Cloud Run service is triggered when files are uploaded to Cloud Storage</summary>

```sh
gsutil -m cp gs://spls/gsp644/* gs://${PROJECT_ID}-upload
```
look in the logs

clean up
```sh
gsutil -m rm gs://${PROJECT_ID}-upload/*
```
</details>

<details><summary>Task 6. Containers</summary>

- modify lots of code in here to get the lab theory stuff correct.
    - modify Dockerfile to install libreoffice
    - modify indext.js
    - libreoffice --headless --convert-to pdf --outdir /tmp
- build it ( gcloud builds submit )
- deploy it ( gcloud run deploy )
```sh
gcloud builds submit \
  --tag gcr.io/${PROJECT_ID}/pdf-converter
```

```sh
gcloud run deploy pdf-converter \
  --image gcr.io/${PROJECT_ID}/pdf-converter \
  --platform managed \
  --region ${REGION} \
  --memory=2Gi \
  --no-allow-unauthenticated \
  --max-instances=1 \
  --set-env-vars PDF_BUCKET=${PROJECT_ID}-processed
```
</details>


<details><summary>Task 7. Testing the pdf-conversion service</summary>

- `curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" $SERVICE_URL`
- copy files... firing off the pub/sub

```sh
curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" $SERVICE_URL
```

```sh
cat <<'EOF' > copy_files.sh
#!/bin/bash

SOURCE_BUCKET="gs://spls/gsp644"
DESTINATION_BUCKET="gs://${GOOGLE_CLOUD_PROJECT}-upload"  # Replace with your actual bucket name
DELAY=5

# Get a list of files in the source bucket
files=$(gsutil ls "$SOURCE_BUCKET")

# Loop through the files
for file in $files; do
  # Construct the full path of the source file
  source_file_path="$file"

  # Copy the file to the destination bucket
  gsutil cp "$source_file_path" "$DESTINATION_BUCKET"

  # Check if the copy was successful
  if [ $? -eq 0 ]; then  # $? is the exit status of the previous command
    echo "Copied: $source_file_path to $DESTINATION_BUCKET"
  else
    echo "Failed to copy: $source_file_path"
  fi

  # Sleep for 5 seconds
  sleep $DELAY
done

echo "All files copied!"
EOF
```

```sh
bash copy_files.sh
```

</details>


