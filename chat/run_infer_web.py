import sys
sys.path.insert(0, '../')  # This is required to import common
# If importing common doesn't go well, check the Python interpreter's current working directory.
# This has to be 'chat' folder.
# import os
# print(os.getcwd())  # print current working directory

#!flask/bin/python
from infer_web import app
from infer_web import controller
import argparse
import nmt.nmt as nmt

parser = argparse.ArgumentParser()
nmt.add_arguments(parser)
FLAGS, unparsed = parser.parse_known_args()

if not FLAGS.out_dir:
#    FLAGS.out_dir = "/Users/ryuji/prg/aplac/chat/generated/4_2316/model"	# MacBookAir13
    FLAGS.out_dir = "/home/apps/prg/aplac/chat/generated/4_2316/model"	# AWS EC2
controller.init(FLAGS)

#Do not add debug=True when VSCode is used. Otherwise breakpoint doesn't hit.
#app.run(debug=True)

if __name__ == '__main__':
    app.run()

