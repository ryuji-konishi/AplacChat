import sys
import nmt.nmt
import argparse
import tensorflow as tf

if __name__ == "__main__":
  nmt_parser = argparse.ArgumentParser()
  nmt.nmt.add_arguments(nmt_parser)
  nmt.nmt.FLAGS, unparsed = nmt_parser.parse_known_args()

  nmt.nmt.FLAGS.inference_input_file="/Users/ryuji/tmp/tensorflow/nmt/nmt_infer/my_infer_file.txt"
  nmt.nmt.FLAGS.inference_output_file="/Users/ryuji/tmp/tensorflow/nmt/nmt_infer/output_infer"
  nmt.nmt.FLAGS.out_dir="/Users/ryuji/tmp/tensorflow/nmt/nmt_model"
  nmt.nmt.FLAGS.num_units=128
  # nmt.nmt.FLAGS.share_vocab=True

  tf.app.run(main=nmt.nmt.main, argv=[sys.argv[0]] + unparsed)

