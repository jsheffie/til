## Labs Completed
| Completed | Title | Location | 
|--------|--------|---|
| 11/01/2025 | [Introduction to Docker](https://www.skills.google/paths/19/course_templates/663/labs/592456) | PCDP -> 10 Deploy Kubernetes Applications on Google Cloud |

### Task 1. Hello world
```sh
gcloud auth list
gcoud config list project
```
export GOOGLE_CLOUD_PROJECT="foo"
export REGION="us-central1"
```sh
docker run hello-world
```

The Docker daemon searched for the hello-world image, didn't find the image locally, pulled the image from a public registry called Docker Hub

Its now local
```sh
docker images
docker run hello-world
```

```sh
docker ps -a
```
them runs are stacking up

```sh
docker run --name [container-name] hello-world
```

### Task 2. Build

```sh
mkdir test && cd test
```

```
cat > Dockerfile <<EOF
# Use an official Node runtime as the parent image
FROM node:lts

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Make the container's port 80 available to the outside world
EXPOSE 80

# Run app.js using node when the container launches
CMD ["node", "app.js"]
EOF
```

Run the following to create the node application:

```
cat > app.js << EOF;
const http = require("http");

const hostname = "0.0.0.0";
const port = 80;

const server = http.createServer((req, res) => {
	res.statusCode = 200;
	res.setHeader("Content-Type", "text/plain");
	res.end("Hello World\n");
});

server.listen(port, hostname, () => {
	console.log("Server running at http://%s:%s/", hostname, port);
});

process.on("SIGINT", function () {
	console.log("Caught interrupt signal and will exit");
	process.exit();
});
EOF
```
Build it

```sh
docker build -t node-app:0.1 .
docker images
```

### Task 3. Run

```sh
docker run -p 4000:80 --name my-app node-app:0.1
```
The -p instructs Docker to map the host's port 4000 to the container's port 80. Now you can reach the server at http://localhost:4000. Without port mapping, you would not be able to reach the container at localhost.

```
curl http://localhost:4000
```

```sh
docker stop my-app && docker rm my-app
```

now run the following command to start the container in the background:

```sh
docker run -p 4000:80 --name my-app -d node-app:0.1
docker ps
```

```sh
docker logs [container_id]
```
Edit app.js with a text editor of your choice (for example nano or vim) and replace "Hello World" with another string:
```
....
const server = http.createServer((req, res) => {
    res.statusCode = 200;
    res.setHeader('Content-Type', 'text/plain');
    res.end('Welcome to Cloud\n');
});
....
```

Rebuild with new tag 0.2
```sh
docker build -t node-app:0.2 .
```

Notice in Step 2 that you are using an existing cache layer. From Step 3 and on, the layers are modified because you made a change in app.js.

Run another container with the new image version. Notice how we map the host's port 8080 instead of 80. You can't use host port 4000 because it's already in use.

```sh
docker run -p 8080:80 --name my-app-2 -d node-app:0.2
docker ps
```
curl http://localhost:8080
```
And now test the first container you made:
```
curl http://localhost:4000
```

```
docker logs -f [container_id]
```

You can use docker exec to do this. Open another terminal (in Cloud Shell, click the + icon) and enter the following command:

```sh
docker exec -it [container_id] bash
```
-it interactive terminal

```
ls
exit
```

```
docker inspect [container_id]
```

Use --format for things
```
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' [container_id]
172.17.0.3
```

### Task 5. Publish (Google Artifact Registery)

### gcloud artifacts repositories create
1. From the Navigation Menu, under CI/CD navigate to Artifact Registry > Repositories.
2. Click the +CREATE REPOSITORY icon next to repositories.
3. Specify my-repository as the repository name.
4. Choose Docker as the format.
5. Under Location Type, select Region and then choose the location : REGION.
6. Click Create.

From the command line
```sh
gcloud artifacts repositories create REPOSITORY_ID \
  --repository-format=FORMAT \
  --location=LOCATION \
  [--description="DESCRIPTION"] \
  [--kms-key="projects/PROJECT/locations/LOCATION/keyRings/KEYRING/cryptoKeys/KEY"] \
  [--async]
```

- `REPOSITORY_ID:` A unique name for the repository (e.g., `my-repo`).
- `--repository-format:` Required; the artifact type (e.g., `docker`).
- `--location:` Required unless set as default; the repository's region.
- `--description:` Optional; a text description.
- `--kms-key:` Optional; for CMEK encryption (otherwise, Google-managed keys are used).
- `--async:` Optional; returns immediately without waiting for completion.

```sh
gcloud artifacts repositories create my-repository2 --repository-format=docker --location=us-central1 --description="Jeff testing delete me" --project=$GCP_PROJECT_NAME

gcloud artifacts repositories create my-repository --repository-format=docker --location="REGION" --description="Docker repository"
```

### gcloud auth configure-docker 
The command updates your Docker configuration. You can now connect with Artifact Registry in your Google Cloud project to push and pull images.

```sh
gcloud auth configure-docker "REGION"-docker.pkg.dev
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### Push the container to Artifact Registry

```sh
export REGION=us-central1
export PROJECT_ID=qwiklabs-gcp-03-ccfe1cd7bc4d
```

```sh
cd ~/test
docker build -t ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-repository/node-app:0.2 .
docker images
docker push ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-repository/node-app:0.2
```

### Test the image

```sh
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
```
You have to remove the child images (of node:lts) before you remove the node image.

```sh
docker rmi ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-repository/node-app:0.2
docker rmi -f $(docker images -aq) # remove remaining images
docker images
```
At this point you should have a pseudo-fresh environment.

```sh
docker run -p 4000:80 -d ${REGION}-docker.pkg.dev/${PROJECT_ID}/my-repository/node-app:0.2
```

```
curl http://localhost:4000
```