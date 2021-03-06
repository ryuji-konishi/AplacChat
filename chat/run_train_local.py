import sys
import nmt.nmt
import argparse
import tensorflow as tf

# data_path = "/Users/ryuji/prg/aplac/chat/generated/4_2316"
data_path = "/Users/ryuji/tmp/aplac/9_Hello"

if __name__ == "__main__":
  nmt_parser = argparse.ArgumentParser()
  nmt.nmt.add_arguments(nmt_parser)
  nmt.nmt.FLAGS, unparsed = nmt_parser.parse_known_args()

  nmt.nmt.FLAGS.src="src"
  nmt.nmt.FLAGS.tgt="tgt"
  nmt.nmt.FLAGS.vocab_prefix=data_path + "/data/vocab"
  nmt.nmt.FLAGS.train_prefix=data_path + "/data/train"
  nmt.nmt.FLAGS.dev_prefix=data_path + "/data/dev"
  nmt.nmt.FLAGS.test_prefix=data_path + "/data/test"
  nmt.nmt.FLAGS.out_dir=data_path + "/model"
  nmt.nmt.FLAGS.num_train_steps=2000
  nmt.nmt.FLAGS.steps_per_stats=100
  nmt.nmt.FLAGS.encoder_type="gnmt"
  nmt.nmt.FLAGS.attention="scaled_luong"
  nmt.nmt.FLAGS.attention_architecture="gnmt_v2"
  nmt.nmt.FLAGS.num_layers=4
  nmt.nmt.FLAGS.num_units=256    # 64: 1.7MB, 1KB, 2.4MB
  nmt.nmt.FLAGS.beam_width=10
  nmt.nmt.FLAGS.length_penalty_weight=1.0
  nmt.nmt.FLAGS.dropout=0.2
  nmt.nmt.FLAGS.metrics="bleu"
  nmt.nmt.FLAGS.share_vocab=True    # This option doesn't work for NMT (git 842c4358695b3da42927e85e7b963a579f8a3363) for tf1.4.0
  nmt.nmt.FLAGS.src_max_len=200
  nmt.nmt.FLAGS.tgt_max_len=200
  nmt.nmt.FLAGS.start_decay_step=50000
  nmt.nmt.FLAGS.decay_steps=10000
  nmt.nmt.FLAGS.decay_factor=0.9

  # Below is the setting for tensorflow/nmt tutorial
  # nmt.nmt.FLAGS.src="vi"
  # nmt.nmt.FLAGS.tgt="en"
  # nmt.nmt.FLAGS.vocab_prefix="/Users/ryuji/tmp/tensorflow/tf_nmt/data/vocab"
  # nmt.nmt.FLAGS.train_prefix="/Users/ryuji/tmp/tensorflow/tf_nmt/data/train"
  # nmt.nmt.FLAGS.dev_prefix="/Users/ryuji/tmp/tensorflow/tf_nmt/data/tst2012"
  # nmt.nmt.FLAGS.test_prefix="/Users/ryuji/tmp/tensorflow/tf_nmt/data/tst2013"
  # nmt.nmt.FLAGS.out_dir="/Users/ryuji/tmp/tensorflow/tf_nmt/model"
  # nmt.nmt.FLAGS.num_train_steps=12000
  # nmt.nmt.FLAGS.steps_per_stats=100
  # nmt.nmt.FLAGS.num_layers=2
  # nmt.nmt.FLAGS.num_units=128
  # nmt.nmt.FLAGS.dropout=0.2
  # nmt.nmt.FLAGS.metrics="bleu"
  # nmt.nmt.FLAGS.share_vocab=True    # This option doesn't work for NMT (git 842c4358695b3da42927e85e7b963a579f8a3363) for tf1.4.0
  # nmt.nmt.FLAGS.src_max_len=200
  # nmt.nmt.FLAGS.tgt_max_len=200


  tf.app.run(main=nmt.nmt.main, argv=[sys.argv[0]] + unparsed)

# The following params are only in FLAGS
#  epoch_step
# The following params are only in argparse, and not saved into hparams file.
#  ckpt
#  hparams_path
#  inference_input_file
#  inference_list
#  inference_output_file
#  inference_ref_file
#  jobid
#  num_workers
#  scope
