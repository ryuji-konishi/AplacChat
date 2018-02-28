
#!/bin/bash

# How to run this script
# Right-click on this file in finder, Get Info, and scroll down to the bottom,
# find the lock icon, click on it and type in the password.
# Next open the terminal, move to the file location, and enter the command:
#  $ chmod 700 this_file.sh

python -m nmt.nmt \
 --src="src" \
 --tgt="tgt" \
 --vocab_prefix="/Users/ryuji/tmp/aplac/data/vocab" \
 --train_prefix="/Users/ryuji/tmp/aplac/data/train" \
 --dev_prefix="/Users/ryuji/tmp/aplac/data/dev" \
 --test_prefix="/Users/ryuji/tmp/aplac/data/test" \
 --out_dir="/Users/ryuji/tmp/aplac/model" \
 --num_train_steps=12000 \
 --steps_per_stats=100 \
 --num_layers=2 \
 --num_units=128 \
 --dropout=0.2 \
 --metrics="bleu" \
 --share_vocab=True \
 --src_max_len=200 \
 --tgt_max_len=200

