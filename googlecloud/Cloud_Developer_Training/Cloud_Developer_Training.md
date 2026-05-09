

<details><summary>01: A Tour of Google Cloud Hands-on Labs</summary>

- This builds a temporary environment in Google Cloud.
    - Start Lab (button)
- When the timer reaches 00:00:00, you lose access to your temporary Google Cloud environment.
    - True
- Some labs have tracking, which scores your completion of hands-on lab activities.
    - True
- In order to receive completion credit for a lab that has tracking, you must complete the required hands-on lab activities.
    - True
- What field is NOT found in the left pane? ( of the lab ) ( which has Project ID, Password, Open Cloud Console)
    - System Admin ( is not on the qwiklab left pane )
- The username in the left panel, which resembles student-xx-xxxxxx@qwiklabs.net, is a Cloud IAM identity.
    - True
- An organizing entity for anything you build with Google Cloud.
    - Google Cloud Project
- 'Qwiklabs Resources' is shared (read only) with all Qwiklabs users, which means that you cannot delete or modify it.
    - True
- 'Qwiklabs Resources' is the project where you run all of your lab steps.
    - False
- IAM & Admin ( Cloud IAM )
    - Identity and Access Management (IAM) [docs](https://cloud.google.com/iam/docs)
- Basic Roles
    - Roles/Viewer
    - Roles/Browser (Optional: not in training materials)
    - Roles/Editor
    - Roles/Owner
- Offers quick access to the platform's services and also outlines its offerings.
    - Navigation Menu ( hamburger )
- Basic roles set project-level permissions and, unless otherwise specified, control access and management to all Google Cloud services.
    - True
- Provides all viewer permissions, plus permissions for actions that modify state, such as changing existing resources.
    - Editor role

- Navigation menu (Navigation menu), click APIs & Services > Library

- When you start a lab, you need to enable APIs in your project to start working with Google Cloud.
    - False

**Links From Lesson**
- [Explore over 150+ Google Cloud products](https://cloud.google.com/products?hl=en#top_of_page)
- [Identity and Access Management documentation](https://cloud.google.com/iam/docs)
- [IAM roles and permissions index](https://cloud.google.com/iam/docs/roles-permissions#primitive\_roles)
- [API design guide](https://cloud.google.com/apis/design/)
- [Google APIs Explorer](https://developers.google.com/apis-explorer/#p/)

</details>

<details><summary>02 Google Cloud Fundamentals: Core Infrastructure</summary>

Why might a Google Cloud customer use resources in several regions around the world?
    - To offer localized application versions in different regions.
    - To earn discounts
    - To improve security
    - * To bring their applications closer to users around the world, and for improved fault tolerance

What is the primary benefit to a Google Cloud customer of using resources in several zones within a region?
    - For getting discounts on other zones
    - For expanding services to customers in new areas
    - For better performance
    - * For improved fault tolerance

What type of cloud computing service lets you bind your application code to libraries that give access to the infrastructure your application needs?
    - Infrastructure as a service
    - * Platform as a service
    - Virtualized data centers
    - Software as a service
    - Hybrid cloud


Choose the correct completion: Services and APIs are enabled on a per-__________ basis.
    - * Project
    - Orginization
    - Folder
    - Billing Account

Order these IAM role types from broadest to finest-grained.
    - Custom roles, predefined roles, basic roles
    - Predefined roles, custom roles, basic roles
    - * Basic roles, predefined roles, custom roles



Which of these values is globally unique, permanent, and unchangeable, but can be modified by the customer during creation?
    - The project's billing credit-card number
    - * The project ID
    - The project name
    - The project number
</details>


In Google Cloud VPCs, what scope do subnets have?
    - Zonal ( nooo )
    - Multi-regional ( nooo)
    - * Regional
    - Global ( noooo ) 

How does Cloud Load Balancing allow you to balance HTTP-based traffic?
    - Across multiple virtual machine instances in a single Compute Engine region.
    - Across multiple Google Cloud Platform services. ( nooo review: Cloud Load Ballancing )
    - * Across multiple Compute Engine regions.
    - Across multiple physical machines in a single data center.

What is the main reason customers choose Preemptible VMs?
    - To improve performance.
    - To reduce cost on premium operating systems.
    - To use custom machine types.
    - * To reduce cost.

For which of these interconnect options is a Service Level Agreement available?
    - Standard Network Tier ( noooo Connecting networks to Google VPC)
    - Carrier Peering
    - * Dedicated Interconnect
    - Direct Peering





```
Hello World!student_04_c37cf19beab5@cloudshell:~/helloworld (qwiklabs-gcp-04-910ec811dc0a)$ history
    1  env |grep PROJECT
    2  gcloud auth list
    3  gcloud config list project
    4  gcloud services info run.googleapis.com
    5  gcloud services
    6  gcloud services list
    7  gcloud services list|grep run
    8  gcloud services enable run.googleapis.com
    9  gcloud config set compute/region us-east1
   10  env |grep LOCATION
   11  export LOCATION="us-east1"
   12  pwd
   13  mkdir helloworld
   14  cd helloworld/
   15  vi package.json
   16  vi index.js
   17  vi Dockerfile
   18  env |grep GOOGLE_CLOUD_PROJECT
   19  gcloud builds submit --tag gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld
   20  gcloud container images list
   21  gcloud auth configure-docker
   22  gcloud container images list
   23  docker run -d -p 8080:8080 gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld
   24  curl localhost:8080
   27  gcloud run deploy --image gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld --allow-unauthenticated --region=$LOCATION
   28  gcloud container images delete gcr.io/$GOOGLE_CLOUD_PROJECT/helloworld
   29  gcloud run services delete helloworld --region=us-east1

   ```

Note:  10: Develope Serverless applications with Firebase
           - Import data to a Firestore datastore
               - /Users/jds/workspace/pet-theory
               - npm install @google-cloud/firestore
               - npm install @google-cloud/logging
               - open: pet-theory/lab01/importTestData.js
               - import const { Firestore } = require("@google-cloud/firestore");
               - gcloud services enable cloudaicompanion.googleapis.com
APIs Explorer: Qwik Start Lab


cat cloudbuild.yaml 
steps:
- name: 'gcr.io/cloud-builders/curl'
  args:
  - '-L'
  - 'https://firebase.tools/bin/linux/latest'
  - '-o'
  - '/workspace/firebase'
- name: 'gcr.io/cloud-builders/curl'
  args:
  - '-L'
  - "https://github.com/gohugoio/hugo/releases/download/v${_HUGO_VERSION}/hugo_extended_${_HUGO_VERSION}_Linux-64bit.tar.gz"
  - '-o'
  - '/workspace/hugo.tar.gz'
  waitFor: ['-']
- name: 'ubuntu:20.04'
  args:
  - 'bash'
  - '-c'
  - |
    tar -xvf /workspace/hugo.tar.gz
    chmod 755 /workspace/firebase
    /workspace/hugo 
    /workspace/firebase deploy --project qwiklabs-gcp-04-c7cd2d115abf --non-interactive --only hosting -m "Build ${BUILD_ID}"
substitutions:
  _HUGO_VERSION: 0.96.0
options:
  defaultLogsBucketBehavior: REGIONAL_USER_OWNED_BUCKET