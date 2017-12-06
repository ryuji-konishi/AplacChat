from common import vocab
from infer_web import app
from flask import request, json
import nmt.utils.misc_utils as utils
from nmt import inference


# Global variables.
hparams = None
infer_model = None
model_dir = None

def init(out_dir):
	global hparams, infer_model, model_dir
	model_dir = out_dir
	# Load hparams.
	hparams = utils.load_hparams(out_dir)
	infer_model = inference.inference_m(out_dir, hparams)

def nmt_inter(inference_input):
	buf_list = vocab.delimit_multi_char_text(inference_input)
	inference_input = vocab.join_list_by_space(buf_list)
	outputs = inference.single_worker_inference_m(
		infer_model,
		model_dir,
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
