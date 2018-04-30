#!/bin/bash

# How to run this script
# Right-click on this file in finder, Get Info, and scroll down to the bottom,
# find the lock icon, click on it and type in the password.
# Next open the terminal, move to the file location, and enter the command:
#  $ chmod 700 this_file.sh


# Work under 'chat' directory.
# /Users/ryuji/prg/aplac/chat

#
# Preparation
#

PROJECT_ID=ryuji-test1
BUCKET_NAME=${PROJECT_ID}-mlengine
REGION=asia-east1
DATA_NAME="11_13158"
DATA_SUBCATEGORY="aplac_conv"
LOCAL_DATA_PATH=/Users/ryuji/tmp/aplac/$DATA_NAME
TRAIN_STEP=200000

# Local directory
#    $DATA_NAME
#        data
#            vocab.src
#            $DATA_SUBCATEGORY
#                train.src
#                train.tgt

# GCP Storage
#    Buckets/$PROJECT_ID-mlengine
#        $DATA_NAME
#            data
#                vocab.src
#                $DATA_SUBCATEGORY
#                    train.src
#                    train.tgt
#            model
#                $JOB_NAME
#                    hparams

#
# Upload the Input Files
#
REMOTE_DATA_PATH=gs://$BUCKET_NAME/$DATA_NAME/data
gsutil -m cp -r "$LOCAL_DATA_PATH/data/vocab.src" "$REMOTE_DATA_PATH"
gsutil -m cp -r "$LOCAL_DATA_PATH/data/$DATA_SUBCATEGORY/*" "$REMOTE_DATA_PATH/$DATA_SUBCATEGORY"

#
# Run the Training Job
#
JOB_NAME=job_$(date +"%y%m%d_%H%M")_${DATA_NAME}_4L512
OUTPUT_PATH=gs://$BUCKET_NAME/$DATA_NAME/model/$JOB_NAME
touch log
gsutil cp ./log "$OUTPUT_PATH/"

gcloud ml-engine jobs submit training $JOB_NAME \
 --job-dir $OUTPUT_PATH \
 --runtime-version 1.4 \
 --package-path nmt \
 --module-name nmt.nmt \
 --region $REGION \
 --config config.yaml \
 -- \
 --src="src" \
 --tgt="tgt" \
 --vocab_prefix="$REMOTE_DATA_PATH/vocab" \
 --train_prefix="$REMOTE_DATA_PATH/$DATA_SUBCATEGORY/train" \
 --dev_prefix="$REMOTE_DATA_PATH/$DATA_SUBCATEGORY/dev" \
 --test_prefix="$REMOTE_DATA_PATH/$DATA_SUBCATEGORY/test" \
 --out_dir="$OUTPUT_PATH" \
 --num_train_steps=$TRAIN_STEP \
 --steps_per_stats=100 \
 --encoder_type="gnmt" \
 --attention="scaled_luong" \
 --attention_architecture="gnmt_v2" \
 --num_layers=4 \
 --residual=True \
 --num_units=512 \
 --beam_width=10 \
 --length_penalty_weight=1.0 \
 --dropout=0.2 \
 --metrics="bleu" \
 --share_vocab=True \
 --src_max_len=200 \
 --tgt_max_len=200 \
 --start_decay_step=100000 \
 --decay_steps=20000 \
 --decay_factor=0.9

#
# Re-training (train again with different data but the same vocab)
#
JOB_NAME=${JOB_NAME}_x
DATA_SUBCATEGORY="conv"
TRAIN_STEP=72000
# And then run the same gcloud command above


#
# Get the Result
#
mkdir $LOCAL_DATA_PATH/model
gsutil -m cp -r $OUTPUT_PATH/* $LOCAL_DATA_PATH/model/

#
# Modify hparams
#
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
