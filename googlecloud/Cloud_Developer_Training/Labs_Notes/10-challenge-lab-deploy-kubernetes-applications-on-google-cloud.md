Deploy Kubernetes Applications on Google Cloud: Challenge Lab

Use valkyrie-app/Dockerfile to create a Docker image called valkyrie-app with the tag v0.0.2.


docker build -t valkyrie-app:v0.0.2 .
docker run -p 8080:8080 valkyrie-app:v0.0.2

Re-Tag
LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE

```sh
export REGION=us-east4
export PROJECT_ID=qwiklabs-gcp-00-4526850f493c
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/valkyrie-docker-repo/valkyrie-app:v0.0.2 .
docker images
gcloud artifacts repositories create valkyrie-docker-repo --repository-format=docker --location=${REGION} --description="valkyrie-docker-repo" --project=$PROJECT_ID

docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/valkyrie-docker-repo/valkyrie-app:v0.0.2
us-east4-docker.pkg.dev/qwiklabs-gcp-00-4526850f493c/valkyrie-docker-repo/valkyrie-app:v0.0.2
export ZONE=us-east4-c
gcloud container clusters get-credentials valkyrie-dev --zone=${ZONE}
-> modify the k8s/deployment.yaml file make the images work
# kubectl create deployment nginx --image=nginx:1.27.0
# kubectl create deployment valkyrie-app --image=valkyrie-app:v0.0.2
-> kubectl create -f k8s/deployment.yaml
-> kubectl create -f k8s/service.yaml
# kubectl expose deployment valkyrie-app --port 80 --type LoadBalancer
# kubectl expose deployment valkyrie-app --port 8080 --type LoadBalancer
```

```sh
# docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-repository/node-app:0.2 .
# docker images
# docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-repository/node-app:0.2 -->
```