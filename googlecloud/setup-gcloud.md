Here is how I installed google-cloud-sdk ( note today, I would just use brew probably )
-----------------------------------------------
```
$ which gcloud
/Users/jeffsheffield/google-cloud-sdk/bin/gcloud
```
```
- Install the Google Cloud SDK https://cloud.google.com/sdk/docs
    - https://cloud.google.com/sdk/docs/install
    - download: extract
    $ cd; mv ~/Downloads/google-cloud-sdk-319.0.0-darwin-x86_64.tar.gz .
    $ tar -zxvf google-cloud-sdk-319.0.0-darwin-x86_64.tar.gz 
    $ rm -f google-cloud-sdk-319.0.0-darwin-x86_64.tar.gz 
    $ cd google-cloud-sdk/
    $ ./install.sh --help
    $ ./install.sh
    Welcome to the Google Cloud SDK!
```
-----------------------------------------------
### My Current State:
```
$ gcloud components list
    Your current Google Cloud CLI version is: 468.0.0
    The latest available version is: 473.0.0
```
-----------------------------------------------
( I would probably do this today: )
```
$ brew upgrade google-cloud-sdk
$gcloud components update
```
[documented here](https://stackoverflow.com/a/78128354
)

