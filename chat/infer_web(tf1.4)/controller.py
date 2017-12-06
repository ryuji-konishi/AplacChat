from common import vocab
from infer_web import app
from flask import request, json
import nmt.nmt as nmt
from nmt import inference
import argparse
import tensorflow as tf

# NMT initialization
FLAGS = None

nmt_parser = argparse.ArgumentParser()
nmt.add_arguments(nmt_parser)
FLAGS, unparsed = nmt_parser.parse_known_args()

FLAGS.out_dir="/Users/ryuji/tmp/aplac/model"
FLAGS.num_units=128
FLAGS.share_vocab=True

# Below is the setting for tensorflow/nmt tutorial
# FLAGS.out_dir="/Users/ryuji/tmp/tensorflow/nmt/nmt_model"
# FLAGS.num_units=128

default_hparams = nmt.create_hparams(FLAGS)

# Load hparams.
hparams = nmt.create_or_load_hparams(
	FLAGS.out_dir, default_hparams, FLAGS.hparams_path, save_hparams=False)

ckpt = tf.train.latest_checkpoint(FLAGS.out_dir)

infer_model = inference.inference_m(ckpt,
	hparams,
	scope=None)

def nmt_inter(inference_input):
	buf_list = vocab.delimit_multi_char_text(inference_input)
	inference_input = vocab.join_list_by_space(buf_list)
	outputs = inference.single_worker_inference_m(
		infer_model,
		ckpt,
		inference_input,
		hparams)
	result = ''
	for o in outputs:
		buf_list = o.split()
		result += vocab.concatenate_multi_char_list(buf_list) + '\n'
	return result.strip()		# remove the last line-break

@app.route('/')
@app.route('/index')
def index():
	return "hello world"

@app.route('/train', methods = ['POST'])
def api_train():
	contentType = request.headers['Content-Type']
	if 'text/plain' in contentType:
		input = request.data.decode('utf-8')
		output = nmt_inter(input)
		return "Text Message: " + output
	elif 'application/json' in contentType:
		return json.dumps(request.json)
	elif 'application/octet-stream' in contentType:
		f = open('./binary', 'wb')
		f.write(request.data)
		f.close()
		return "Binary message written!"
	else:
		return "415 Unsupported Media Type " + contentType

@app.route('/echo', methods = ['POST'])
def api_echo():
	contentType = request.headers['Content-Type']
	if 'text/plain' in contentType:
		return "Text Message: " + request.data.decode('utf-8')
	elif 'application/json' in contentType:
		return json.dumps(request.json)
	elif 'application/octet-stream' in contentType:
		f = open('./binary', 'wb')
		f.write(request.data)
		f.close()
		return "Binary message written!"
	else:
		return "415 Unsupported Media Type " + contentType
