import sys
import nmt.nmt
import argparse
import tensorflow as tf

if __name__ == "__main__":
  nmt_parser = argparse.ArgumentParser()
  nmt.nmt.add_arguments(nmt_parser)
  nmt.nmt.FLAGS, unparsed = nmt_parser.parse_known_args()

  data_path = "/Users/ryuji/tmp/aplac/9_Hello"
  nmt.nmt.FLAGS.inference_input_file=data_path + "/infer/my_infer_file.txt"
  nmt.nmt.FLAGS.inference_output_file=data_path + "/infer/output_infer.txt"
  nmt.nmt.FLAGS.out_dir=data_path + "/model"

  tf.app.run(main=nmt.nmt.main, argv=[sys.argv[0]] + unparsed)

