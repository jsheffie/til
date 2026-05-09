## Labs Completed
| Completed | Title | Location | 
|--------|--------|---|
| 11/01/2025 | [Orchestrating the Cloud with Kubernetes](https://www.skills.google/paths/19/course_templates/663/labs/592458) | PCDP -> 10 Deploy Kubernetes Applications on Google Cloud |


```sh
gcloud auth list
gcloud config list project
```

<details><summary>Task 1. Google Kubernetes Engine</summary>

Your [compute zone](https://cloud.google.com/compute/docs/regions-zones/#available) is an approximate regional location in which your clusters and their resources live. For example, us-central1-a is a zone in the us-central1 region.


```sh
export REGION=us-central1
export ZONE=us-central1-a

gcloud config set compute/zone ${ZONE}
```

Start up the cluster for ths lab
```sh
export CLUSTER_NAME=io
gcloud container clusters create ${CLUSTER_NAME} --zone ${ZONE}
```

```
Created [https://container.googleapis.com/v1/projects/qwiklabs-gcp-00-cbe082067474/zones/us-west1-c/clusters/io].
To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/us-west1-c/io?project=qwiklabs-gcp-00-cbe082067474
kubeconfig entry generated for io.
NAME: io
LOCATION: us-west1-c
MASTER_VERSION: 1.33.5-gke.1162000
MASTER_IP: 136.117.170.47
MACHINE_TYPE: e2-medium
NODE_VERSION: 1.33.5-gke.1162000
NUM_NODES: 3
STATUS: RUNNING
STACK_TYPE: IPV4
```
You are automatically authenticated to your cluster upon creation. If you lose connection to your Cloud Shell for any reason, run the `gcloud container clusters get-credentials io` command to re-authenticate.

```sh
re-authenticate w/ 
gcloud container clusters get-credentials ${CLUSTER_NAME}
```

Note: It will take a while to create a cluster - Kubernetes Engine is provisioning a few Virtual Machines behind the scenes for you to play with!

</details>

<details><summary>Task 1.1. Get the sample code</summary>

```sh
gcloud storage cp -r gs://spls/gsp021/* .
cd orchestrate-with-kubernetes/kubernetes
ls -R
.:
cleanup.sh  deployments  nginx  pods  services  tls

./deployments:
auth.yaml  fortune-service.yaml  frontend.yaml

./nginx:
frontend.conf  proxy.conf

./pods:
fortune-app.yaml  secure-fortune.yaml

./services:
auth.yaml  fortune-app.yaml  fortune-service.yaml  frontend.yaml  monolith.yaml

./tls:
ca-key.pem  ca.pem  cert.pem  key.pem

```
Now that you have the code -- it's time to give Kubernetes a try!

</details>

### Task 2. A quick Kubernetes demo

The easiest way to get started with Kubernetes is to use the kubectl create command.
1. Use it to launch a single instance of the nginx container:

```sh
kubectl create deployment nginx --image=nginx:1.27.0
```

Kubernetes has created a Deployment
Deployments keep the Pods up and running even when the nodes they run on fail.


In Kubernetes, all containers run in a Pod.

2. Use the kubectl get pods command to view the running nginx container:

```sh
kubectl get pods
```

3. Once the nginx container has a Running status you can expose it outside of Kubernetes using the kubectl expose command:

```sh
kubectl expose deployment nginx --port 80 --type LoadBalancer
```
So what just happened? Behind the scenes Kubernetes created an external load balancer with a public IP address attached to it. Any client who hits that public IP address will be routed to the Pods behind the service. In this case that would be the nginx Pod.

4. List the services now using the kubectl get services command:

```sh
kubectl get services
```

5. Add the External IP to this command to hit the Nginx container remotely:
```sh
curl http://<External IP>:80
```

### Task 3. About Pods
At the core of Kubernetes is the Pod.

### Task 4. Create Pods

### Task 5. Interact with Pods

### Task 6. About Services

### Task 7. Create a Service

### Task 8. Add labels to Pods

### Task 9. About Deployments

### Task 10. Create Deployments