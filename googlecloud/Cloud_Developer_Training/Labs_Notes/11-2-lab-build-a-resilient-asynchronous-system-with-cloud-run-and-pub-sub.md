## Labs Completed
| Completed | Title | Location | 
|--------|--------|---|
| 11/02/2025 | [2 Build a Resilient, Asynchronous System with Cloud Run and Pub/Sub](https://www.skills.google/paths/19/course_templates/741/labs/592445) | PCDP -> 11 Develop Serverless Applications on Cloud Run |


```sh
gcloud config set compute/zone "us-west1-c"
export ZONE=$(gcloud config get compute/zone)

gcloud config set compute/region "us-west1"
export REGION=$(gcloud config get compute/region)
```


gcloud pubsub subscriptions create email-service-sub --topic new-lab-report --push-endpoint=$EMAIL_SERVICE_URL --push-auth-service-account=pubsub-cloud-run-invoker@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com
gcloud pubsub subscriptions create sms-service-sub   --topic new-lab-report --push-endpoint=$SMS_SERVICE_URL   --push-auth-service-account=pubsub-cloud-run-invoker@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com