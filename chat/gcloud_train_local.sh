#!/bin/bash

# How to run this script
# Right-click on this file in finder, Get Info, and scroll down to the bottom,
# find the lock icon, click on it and type in the password.
# Next open the terminal, move to the file location, and enter the command:
#  $ chmod 700 this_file.sh

# Python3 tf1.4, Python2 tf1.4
DATA_NAME="5_0314"
LOCAL_DATA_PATH="generated/$DATA_NAME/data"
LOCAL_OUTPUT_PATH="generated/$DATA_NAME/model"

gcloud ml-engine local train --package-path char --module-name nmt.nmt \
 -- \
 --src="src" \
 --tgt="tgt" \
 --vocab_prefix="$LOCAL_DATA_PATH/vocab" \
 --train_prefix="$LOCAL_DATA_PATH/train" \
 --dev_prefix="$LOCAL_DATA_PATH/train" \
 --test_prefix="$LOCAL_DATA_PATH/train" \
 --out_dir="$LOCAL_OUTPUT_PATH" \
 --num_train_steps=12000 \
 --steps_per_stats=100 \
 --num_layers=2 \
 --num_units=128 \
 --dropout=0.2 \
 --metrics="bleu" \
 --share_vocab=True \
 --src_max_len=200 \
 --tgt_max_len=200




