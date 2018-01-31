# Setup Chat on Google Cloud Platform (GCP)

This document describes how to deploy the Chat component on to Google Cloud Platform and run it for the purpose of NMT Training.

## Basic Idea

To run a Python program on GCP, you need Google Cloud SDK and you will use its primary command 'gsutil'. With this command you can do the following tasks.
* Run your program locally
* Upload your program on to GCP and run it
* Upload/Download files to/from Google Cloud Storage

Google Cloud Storage (GCS) is used to store the input/output files that are required by your program when running on GCP. Thus your program has to be configurable in the file paths that are given by the program command argument. In case of our NMT Training those files include the input files (source, target, vocaburary) and the various generated files.
So, to run the Chat program, you need to first upload the input files on to GCS. And after running the Chat program, you need to download the generated files from GCS.

The all above described tasks are done by the Google Cloud SDK command 'gsutil', and thus the following sections describe the command usage running on the shell script.
Here the running environment is MacOS.

## Preparation

In your terminal, run the commands below before proceeding. Those symbols will be used in the later sections.

Assuming you already have a cloud project on GCP, and in this document it's named as 'ryuji-test1'.
```
PROJECT_ID=ryuji-test1
```
To access to GCS, you need to create a bucket. Here we have the bucket name defined as below.
```
BUCKET_NAME=${PROJECT_ID}-mlengine
```
Choose the GCP region where your program and GCS files are located.
```
REGION=asia-east1
```
Define a data folder name where all files are stored. During the training phase, you will want to try many different data sets and see how the training went on. So here we define a folder where the input/output of training files are stored. Also you will end up in having multiple folders within the single bucket.
```
DATA_NAME="4_2316"
```

## Create Google Cloud Storage

Now create a new bucket in GCS with the command below. Once created you don't need to create another one unless required.
```
gsutil mb -l $REGION gs://$BUCKET_NAME
```
In this bucket, a new folder will be created with the name of ```$DATA_NAME``` once you run Chat. Each folder will contain the input for the NMT Training and the result of the NMT Taining.

## Upload the Input Files

Upload the input files which you prepaired in advance and are located in ```generated/$DATA_NAME``` under the current directory.
The remote directory in GCS is ```gs://$BUCKET_NAME/data``` constant.
```
LOCAL_DATA_PATH="generated/$DATA_NAME"
REMOTE_DATA_PATH=gs://$BUCKET_NAME/data
gsutil -m cp -r "$LOCAL_DATA_PATH/data/*" "$REMOTE_DATA_PATH"
```
