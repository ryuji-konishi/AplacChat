
#!/bin/bash

# How to run this script
# Right-click on this file in finder, Get Info, and scroll down to the bottom,
# find the lock icon, click on it and type in the password.
# Next open the terminal, move to the file location, and enter the command:
#  $ chmod 700 this_file.sh

DATA_PATH="/Users/ryuji/tmp/aplac/9_Hello"

python -m nmt.nmt \
 --src="src" \
 --tgt="tgt" \
 --vocab_prefix="${DATA_PATH}/data/vocab" \
 --train_prefix="${DATA_PATH}/data/train" \
 --dev_prefix="${DATA_PATH}/data/dev" \
 --test_prefix="${DATA_PATH}/data/test" \
 --out_dir="${DATA_PATH}/model" \
 --num_train_steps=1000 \
 --steps_per_stats=100 \
 --num_layers=2 \
 --num_units=128 \
 --dropout=0.2 \
 --metrics="bleu" \
 --share_vocab=True \
 --src_max_len=200 \
 --tgt_max_len=200

