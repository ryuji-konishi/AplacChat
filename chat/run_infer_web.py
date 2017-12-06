import sys
sys.path.insert(0, '../')  # This is required to import common
#!flask/bin/python
from infer_web import app
from infer_web import controller
import argparse

parser = argparse.ArgumentParser()
# This script requires the argument 'out_dir' only
parser.add_argument("--out_dir", type=str, default=None, help="Store log/model files.")
FLAGS, unparsed = parser.parse_known_args()
if not FLAGS.out_dir:
    FLAGS.out_dir = "/Users/ryuji/prg/aplac/chat/generated/4_2316/model"	# MacBookAir13
    FLAGS.out_dir = "/home/apps/prg/aplac/chat/generated/4_2316/model"	# AWS EC2
controller.init(FLAGS.out_dir)

#Do not add debug=True when VSCode is used. Otherwise breakpoint doesn't hit.
#app.run(debug=True)

if __name__ == '__main__':
    app.run()

