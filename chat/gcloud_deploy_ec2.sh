
#
# Preparation
#
PROJECT_ID=ryuji-test1
BUCKET_NAME=${PROJECT_ID}-mlengine
REGION=asia-east1
DATA_NAME="10_12974"
LOCAL_DATA_PATH="generated/$DATA_NAME"
JOB_NAME="job_180415_090124_10_12974_standard_gpu_x_x_x"

#
# Copy from GCP Storage
#
REMOTE_DATA_PATH=gs://$BUCKET_NAME/$DATA_NAME/data
OUTPUT_PATH=gs://$BUCKET_NAME/$DATA_NAME/model/$JOB_NAME

mkdir $LOCAL_DATA_PATH/model
gsutil -m cp -r dir $OUTPUT_PATH/* $LOCAL_DATA_PATH/model/
mkdir $LOCAL_DATA_PATH/data
gsutil -m cp -r $REMOTE_DATA_PATH/* $LOCAL_DATA_PATH/data/

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
