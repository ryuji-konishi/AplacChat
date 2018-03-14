# Chat Component

## Python Modules
### nmt
Basically this is a copy of Tensorflow tutorial [Neural Machine Translation (seq2seq)](https://github.com/tensorflow/nmt).

### infer_web
The main module to run NMT inference on web server. [Flask](http://flask.pocoo.org/) is used as the web server framework.
This module calls the custom inference methods in nmt module. Those customized methods are named with '_m' post-fix.

## Notes

### How to run tensorboard
```
$ tensor board --logdir=/tmp/aplac/model
```
### Files

#### 'run_infer_web.py'
A Python module 'infer_web' is executed.
The entry point of inference to be continuously running on the web.

#### 'run_infer_local.py'
A Python module 'nmt' is executed.
A tester script for inference. Read input from file and emit output into file.
This script is mainly for local debugging with IDE.

#### 'run_train_local.py'
A Python module 'nmt' is executed.
A tester script for training. Read input from file and emit output into file.
This script is mainly for local debugging with IDE.

#### 'run_train.sh'
Equivalant to 'run_train.py' but it's a shell script for Mac OS.

#### 'chat.service'
This is a Linux SystemD daemon service definition file, used when a daemon is registered.
