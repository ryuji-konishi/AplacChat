# Script commands that run on the target deployment machine.

#
# Preparation
#
PROJECT_ID=ryuji-test1
BUCKET_NAME=${PROJECT_ID}-mlengine
REGION=asia-east1
DATA_NAME="11_13158"
LOCAL_DATA_PATH=/home/aplac/data/$DATA_NAME
JOB_NAME="job_180425_2041_11_13158_4L512"

#
# Copy from GCP Storage
#
REMOTE_DATA_PATH=gs://$BUCKET_NAME/$DATA_NAME/data
OUTPUT_PATH=gs://$BUCKET_NAME/$DATA_NAME/model/$JOB_NAME

mkdir -p $LOCAL_DATA_PATH/model
gsutil -m cp -r $OUTPUT_PATH/* $LOCAL_DATA_PATH/model/
mkdir -p $LOCAL_DATA_PATH/data
gsutil -m cp -r $REMOTE_DATA_PATH/vocab.src $LOCAL_DATA_PATH/data/vocab.src

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
