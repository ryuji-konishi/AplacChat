import sys
sys.path.insert(0, '..\\')  # This is required to import common

import os
import argparse
import commands.compile as compile
import commands.parse as parse
import commands.clean as clean

def add_arguments(parser):
    """Build ArgumentParser."""
    parser.add_argument("--mode", type=str, default="all", help="""\
      uni | bi | gnmt. For bi, we build num_layers/2 bi-directional layers.For
      gnmt, we build 1 bi-directional layer, and (num_layers - 1) uni-
      directional layers.\
      """)

if __name__ == "__main__":
    print ('build started.')
    arg_parser = argparse.ArgumentParser()
    add_arguments(arg_parser)
    args = arg_parser.parse_args()
    
    # current_dir = os.path.dirname(os.path.realpath(__file__))
    html_dir = "C:\\Tmp\\aplac\\html\\xs"
    corpus_dir = "C:\\Tmp\\aplac\\corpus\\xs"
    data_dir = "C:\\Tmp\\aplac\\data\\xs"

    if args.mode == 'all':
        clean.run(html_dir)
        parse.run(html_dir, corpus_dir)
        compile.run(corpus_dir, data_dir)
    elif args.mode == 'clean':
        clean.run(html_dir)
    elif args.mode == 'parse':
        parse.run(html_dir, corpus_dir)
    elif args.mode == 'compile':
        compile.run(corpus_dir, data_dir)
    else:
        print (args.mode)

print ("Finished.")
