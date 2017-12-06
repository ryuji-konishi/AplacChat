#!/bin/bash

# This script is for preparing the Google Cloud Platform environment for the purposes
# of running Training of APLaC.

# How to run this script
# Right-click on this file in finder, Get Info, and scroll down to the bottom,
# find the lock icon, click on it and type in the password.
# Next open the terminal, move to the file location, and enter the command:
#  $ chmod 700 this_file.sh

PROJECT_ID=ryuji-test1
BUCKET_NAME=${PROJECT_ID}-mlengine
REGION=asia-east1

# Create a cloud storage.
gsutil mb -l $REGION gs://$BUCKET_NAME

# Upload files to the cloud storage.
# The files are in advance generated within generated folder.
DATA_NAME="4_2316"
LOCAL_DATA_PATH="generated/$DATA_NAME"
REMOTE_DATA_PATH=gs://$BUCKET_NAME/data
gsutil -m cp -r "$LOCAL_DATA_PATH/data/*" "$REMOTE_DATA_PATH"

# Check uploaded files in storage
# https://console.cloud.google.com/storage

# Run the initial job
JOB_NAME=job_$(date +"%y%m%d_%H%M%S")_$DATA_NAME
OUTPUT_PATH=gs://$BUCKET_NAME/model/$JOB_NAME

# A file 'log' has to exist in storage otherwise the NMT program fails at train.py line 192.
# Create an empty file and upload it to storage in advance.
touch log
gsutil cp ./log "$OUTPUT_PATH/"

gcloud ml-engine jobs submit training $JOB_NAME \
 --job-dir $OUTPUT_PATH \
 --runtime-version 1.2 \
 --package-path nmt \
 --module-name nmt.nmt \
 --region $REGION \
 -- \
 --src="src" \
 --tgt="tgt" \
 --vocab_prefix="$REMOTE_DATA_PATH/vocab" \
 --train_prefix="$REMOTE_DATA_PATH/train" \
 --dev_prefix="$REMOTE_DATA_PATH/dev" \
 --test_prefix="$REMOTE_DATA_PATH/test" \
 --out_dir="$OUTPUT_PATH" \
 --num_train_steps=12000 \
 --steps_per_stats=100 \
 --num_layers=2 \
 --num_units=128 \
 --dropout=0.2 \
 --metrics="bleu" \
 --src_max_len=200 \
 --tgt_max_len=200

# Check Jobs
# https://console.cloud.google.com/mlengine/jobs

# Download files from Cloud Storage
mkdir $LOCAL_DATA_PATH/model
gsutil -m cp -r dir $OUTPUT_PATH/* $LOCAL_DATA_PATH/model/

# The hparams file downloaded from storage contains the file path for Cloud Storage.
# Now you need to update hparams file with local directory settings.
HPARAMS=$LOCAL_DATA_PATH/model/hparams
cp $HPARAMS ${HPARAMS}_gcp      # take backup

# Replace $OUTPUT_PATH -> $LOCAL_DATA_PATH/model
S1=$(echo $OUTPUT_PATH | sed 's=/=\\/=g')
S2=$(echo $LOCAL_DATA_PATH/model | sed 's=/=\\/=g')
sed -i -- "s/$S1/$S2/g" $HPARAMS

# Replace $REMOTE_DATA_PATH -> $LOCAL_DATA_PATH/data
S1=$(echo $REMOTE_DATA_PATH | sed 's=/=\\/=g')
S2=$(echo $LOCAL_DATA_PATH/data | sed 's=/=\\/=g')
sed -i -- "s/$S1/$S2/g" $HPARAMS

# Start running inference web server
python run_infer_web.py --out_dir=$LOCAL_DATA_PATH/model


