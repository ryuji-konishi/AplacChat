import sys
sys.path.insert(0, '..\\')  # This is required to import common

import os
import argparse
import commands.compile as compile
import commands.parse as parse
import commands.clean as clean

def conv_abs(path):
    """ Check if path is relative path, and convert it to absolute path 
        based on the current working directory (the user is working in the terminal).
    """
    if not os.path.isabs(path):
        current_path = os.getcwd()
        path = os.path.join(current_path, path)
        path = os.path.realpath(path)       # this is to remove '../'
    return path

def _all(args):
    """ Function called when the 'all' command is set in the argument."""
    html_dir = conv_abs(args.html)
    corpus_dir = conv_abs(args.corpus)
    data_dir = conv_abs(args.data)

    clean.run(html_dir)
    parse.run(html_dir, corpus_dir)
    compile.run(corpus_dir, data_dir)

def _clean(args):
    """ Function called when the 'clean' command is set in the argument."""
    html_dir = conv_abs(args.html)

    clean.run(html_dir)

def _parse(args):
    """ Function called when the 'parse' command is set in the argument."""
    html_dir = conv_abs(args.html)
    corpus_dir = conv_abs(args.corpus)

    parse.run(html_dir, corpus_dir)

def _compile(args):
    """ Function called when the 'compile' command is set in the argument."""
    corpus_dir = conv_abs(args.corpus)
    data_dir = conv_abs(args.data)

    compile.run(corpus_dir, data_dir)

def add_arguments(parser):
    """Build ArgumentParser."""

    # Help descriptions
    help_all = "Execute the all tree commands in the order of clean, parse and compile."
    help_clean = "Clean the HTML files by eliminating garbage files and also check if all files are valid and readable."
    help_parse = "Parse the HTML files and generate corpus files."
    help_compile = "Read corpus files and generate the NMT data files (src/tgt/vocab)."

    help_html = "HTML files to parse. Absolute or relative path to a directory that contains HTML files, or a single HTML file."
    help_corpus = "Corpus files processed during build. Absolute or relative path to a directory where the corpus files are generated and read from."
    help_data = "Data files (src/tgt/vocab) generated as outcome. Absolute or relative path to a directory where the data files are generated."

    subparsers = parser.add_subparsers(help="Choose command from below.", dest='command')

    # create the parser for the "all" command
    parser_all = subparsers.add_parser('all', help=help_all)
    parser_all.add_argument('html', type=str, help=help_html)
    parser_all.add_argument('corpus', type=str, help=help_corpus)
    parser_all.add_argument('data', type=str, help=help_data)
    parser_all.set_defaults(func = _all)

    # create the parser for the "clean" command
    parser_clean = subparsers.add_parser('clean', help=help_clean)
    parser_clean.add_argument('html', type=str, help=help_html)
    parser_clean.set_defaults(func = _clean)

    # create the parser for the "parse" command
    parser_parse = subparsers.add_parser('parse', help=help_parse)
    parser_parse.add_argument('html', type=str, help=help_html)
    parser_parse.add_argument('corpus', type=str, help=help_corpus)
    parser_parse.set_defaults(func = _parse)

    # create the parser for the "compile" command
    parser_compile = subparsers.add_parser('compile', help=help_compile)
    parser_compile.add_argument('corpus', type=str, help=help_corpus)
    parser_compile.add_argument('data', type=str, help=help_data)
    parser_compile.set_defaults(func = _compile)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    add_arguments(arg_parser)
    args = arg_parser.parse_args()
    args.func(args)     # func is a function pointer which is set for each command with set_defaults function.

print ("Finished.")
