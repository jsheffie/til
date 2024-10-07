
[Artifact Registry documentation](https://cloud.google.com/artifact-registry/docs)

[Store Docker container images in Artifact Registry](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images)

Start with **Guide Me**
1. Create a Docker repository in Artifact Registry.
2. Set up authentication.
3. Push an image to the repository.
4. Pull the image from the repository.

10 Steps
1. Google Cloud Project Setup ( $GCP_PROJECT_NAME )
   - Enable the Artifact Registry API:
2. Set up Cloud Shell
   - It comes pre-installed with Docker and the gcloud CLI, the primary command-line interface for Google Cloud.
3. Create a Docker repository using Cloud Console
4. Configure authentication
   You can now connect with Artifact Registry in your Google Cloud project to push and pull images.
5. Obtain an image to push
6. Tag the image for the repository
7. Push the image to the artifact registory
8. Pull the image from Artifact Registry
9. Success


**Step 2: Verifying cloud shell**
```sh
export GCP_PROJECT_NAME=my-nifty-project-name
$ gcloud artifacts repositories list --project=$GCP_PROJECT_NAME
```

**Step 3:** [Create repository](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images#create)
```sh
$ gcloud artifacts repositories create quickstart-docker-repo --repository-format=docker --location=us-central1 --description="Jeff testing delete me" --project=$GCP_PROJECT_NAME
    Create request issued for: [quickstart-docker-repo]
    Waiting for operation [projects/$GCP_PROJECT_NAME/locations/us-central1/operations/<hash>] to complete...done.   
    Created repository [quickstart-docker-repo].
```

**Step 4: Configure authentication**
```sh
$ gcloud auth configure-docker us-central1-docker.pkg.dev

After update, the following will be written to your Docker config file located at [/Users/jds/.docker/config.json]
... added "us-central1-docker.pkg.dev": "gcloud" to "credHelpers"
```
**Step 5: Obtain an image to push**
```sh
$ docker pull us-docker.pkg.dev/google-samples/containers/gke/hello-app:1.0
  Downloaded newer image for us-docker.pkg.dev/google-samples/containers/gke/hello-app:1.0
```
**Step 6: Tag the image for the repository**
```sh
$ docker images
$ docker tag us-docker.pkg.dev/google-samples/containers/gke/hello-app:1.0 \
    us-central1-docker.pkg.dev/$GCP_PROJECT_NAME/quickstart-docker-repo/quickstart-image:tag1
```

| Repository Host Location | Hostname       | Cloud Project ID | Repository ID          | docker image name | Tag Name |
|------------------------- | -------------- | ---------------- | ---------------------- | ----------------- | --- |
| us-central1              | docker.pkg.dev | $GCP_PROJECT_NAME | quickstart-docker-repo | quickstart-image  | tag1 |

**Step 7: Push the image to the artifact registory**

```sh
$ docker push us-central1-docker.pkg.dev/$GCP_PROJECT_NAME/quickstart-docker-repo/quickstart-image:tag1
```

**Step 8: Pull the image from the artifact registory**

```sh
$ docker images
$ docker image rm us-central1-docker.pkg.dev/$GCP_PROJECT_NAME/quickstart-docker-repo/quickstart-image:tag1

$ docker pull us-central1-docker.pkg.dev/$GCP_PROJECT_NAME/quickstart-docker-repo/quickstart-image:tag1
$ docker images
```

```sh                         
$ gcloud artifacts docker images list us-central1-docker.pkg.dev/$GCP_PROJECT_NAME/quickstart-docker-repo --project=$GCP_PROJECT_NAME

IMAGE                                                                                DIGEST                                                                   CREATE_TIME          UPDATE_TIME          SIZE
us-central1-docker.pkg.dev/$GCP_PROJECT_NAME/quickstart-docker-repo/quickstart-image  sha256:ae6185793ba75c682897ec485e138c678b5b8099ceecc6195ec3be779f10ac01  2024-10-04T10:30:00  2024-10-04T10:30:00  12784423
```

## Real World...
I built an ffmpeg image on my local desktop
1. tag it.
2. push it.
3. pull it. ( and add it to our base images pull )

```sh
Tag it
$ docker tag ffmpeg-7.1-ubuntu2404-desktop-build:latest us-central1-docker.pkg.dev/$GCP_PROJECT_NAME/docker-repo/ffmpeg-7.1-ubuntu2404-desktop-build:1.0.0

push it
$ docker push us-central1-docker.pkg.dev/$GCP_PROJECT_NAME/docker-repo/ffmpeg-7.1-ubuntu2404-desktop-build:1.0.0

```