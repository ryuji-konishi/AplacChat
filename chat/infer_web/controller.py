from common import tokenizer as tk
from common import utils
from infer_web import app
from flask import request, json, jsonify
import nmt.nmt as nmt
from nmt import inference
import argparse
import tensorflow as tf

hparams = None
ckpt = None
infer_model = None
tokenizer = tk.tokenizer()

def init(FLAGS):
	global hparams, ckpt, infer_model
	FLAGS.num_units=128
	FLAGS.share_vocab=True

	default_hparams = nmt.create_hparams(FLAGS)
	# Load hparams.
	hparams = nmt.create_or_load_hparams(
		FLAGS.out_dir, default_hparams, FLAGS.hparams_path, save_hparams=False)

	ckpt = tf.train.latest_checkpoint(FLAGS.out_dir)

	infer_model = inference.inference_m(ckpt,
		hparams,
		scope=None)

def nmt_inter(inference_input):
	buf_list = tokenizer.split(inference_input)
	inference_input = utils.join_list_by_space(buf_list)
	outputs = inference.single_worker_inference_m(
		infer_model,
		ckpt,
		inference_input,
		hparams)
	result = ''
	for o in outputs:
		buf_list = o.split()
		result += tokenizer.concatenate(buf_list) + '\n'
	return result.strip()		# remove the last line-break

@app.route('/')
@app.route('/index')
def index():
	return "hello world"

@app.route('/infer', methods = ['POST'])
def api_infer():
	contentType = request.headers['Content-Type']
	if 'text/plain' in contentType:
		input = request.data.decode('utf-8')
		output = nmt_inter(input)
		print(output.encode('utf-8'))
		resp = jsonify(output)
		resp.headers.add('Access-Control-Allow-Origin', '*')
		return resp
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
