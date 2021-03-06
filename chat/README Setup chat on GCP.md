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

In this section we are going to define several symbols as the shell script environment variables. Those symbols will be used in the later sections. The current terminal directory is set as below.
```
$ pwd
/Users/ryuji/prg/aplac/chat
```
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
Define a local folder name where the input files are stored. During the training phase, you will want to try many different data sets and see how the training went on. So here we define a folder name where the input files of each training are stored.
```
DATA_NAME="4_2316"
```
Define a subcategory name of the data. This sub-categorization is useful when you pre-train or post-train the same dataset without changing the vocaburary.
```
DATA_SUBCATEGORY="aplac_conv"
```
In the end, the local data path becomes below.
```
LOCAL_DATA_PATH=/Users/ryuji/tmp/aplac/$DATA_NAME
```
The train step is defined here so that you can increase the number when you would re-train.
```
TRAIN_STEP=200000
```

## Create Google Cloud Storage

Now create a new bucket in GCS with the command below. Once created you don't need to create another one unless required.
```
gsutil mb -l $REGION gs://$BUCKET_NAME
```
In this bucket, the following two folders will be created in the end.
* 'data' - The folder containing input files. The files are placed directly under this folder and no sub-folders will be created.
* 'model' - The folder containing the output. At every run a sub-folder with job name is created, and the all output is placed here.

### Local directory
```
    $DATA_NAME
        data
            vocab.src
            $DATA_SUBCATEGORY
                train.src
                train.tgt
```
### GCP Storage
```
    Buckets/$PROJECT_ID-mlengine
        $DATA_NAME
            data
                vocab.src
                $DATA_SUBCATEGORY
                    train.src
                    train.tgt
            model
                $JOB_NAME
                    hparams
```

## Upload the Input Files

Upload the input files which you prepaired in advance and are located in ```$LOCAL_DATA_PATH```.

The remote directory in GCS ```$REMOTE_DATA_PATH``` is defined below.
```
REMOTE_DATA_PATH=gs://$BUCKET_NAME/$DATA_NAME/data
REMOTE_DATA_PATH=gs://$BUCKET_NAME/$DATA_NAME/data
gsutil -m cp -r "$LOCAL_DATA_PATH/data/vocab.src" "$REMOTE_DATA_PATH"
gsutil -m cp -r "$LOCAL_DATA_PATH/data/$DATA_SUBCATEGORY/*" "$REMOTE_DATA_PATH/$DATA_SUBCATEGORY"
```

After running the command, you can check the storage contents [here](https://console.cloud.google.com/storage).

## Run the Training Job
The job is named after the current date and time.
```
JOB_NAME=job_$(date +"%y%m%d_%H%M")_${DATA_NAME}
OUTPUT_PATH=gs://$BUCKET_NAME/$DATA_NAME/model/$JOB_NAME
```

A file 'log' has to exist in storage otherwise the NMT program fails at train.py line 192. Create an empty file and upload it to storage in advance.
```
touch log
gsutil cp ./log "$OUTPUT_PATH/"
```

Now run the job. Notice GPU is used.
```
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
```

You can check the jobs [here](https://console.cloud.google.com/mlengine/jobs)

## Get the Result

Download the generated files (model folder) from GCS to local.
```
mkdir $LOCAL_DATA_PATH/model
gsutil -m cp -r $OUTPUT_PATH/* $LOCAL_DATA_PATH/model/
```

If data folder download is required:
```
mkdir $LOCAL_DATA_PATH/data
gsutil -m cp -r $REMOTE_DATA_PATH/* $LOCAL_DATA_PATH/data/
```

### Modify HParams Paths
The ```hparams``` file downloaded from storage contains the file path for Cloud Storage which is different from the local directory settings. This means that you can't run Chat locally to see the result of training. Replace the directory path from GCS to local.
```
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
```

## Try Inference with the Resulted Data
Start the inference web server locally with the training data you just downloaded.
```
python run_infer_web.py --out_dir=$LOCAL_DATA_PATH/model/$JOB_NAME
```






