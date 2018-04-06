import sys
sys.path.insert(0, '..\\')  # This is required to import common

import os
import argparse
import commands.compile as compile
import commands.parse as parse
import commands.clean as clean
import commands.generate as generate

def conv_abs(path):
    """ Check if path is relative path, and convert it to absolute path 
        based on the current working directory (the user is working in the terminal).
    """
    if not os.path.isabs(path):
        current_path = os.getcwd()
        path = os.path.join(current_path, path)
        path = os.path.realpath(path)       # this is to remove '../'
    return path

def f_aplac(args):
    """ Function called when the 'all' command is set in the argument."""
    html_dir = conv_abs(args.html)
    corpus_dir = conv_abs(args.corpus)
    data_dir = conv_abs(args.data)

    clean.run(html_dir)
    parse.run(html_dir, corpus_dir)
    compile.run(corpus_dir, data_dir)

def f_html_clean(args):
    """ Function called when the 'html clean' command is set in the argument."""
    html_dir = conv_abs(args.html)

    clean.run(html_dir)

def f_html_parse(args):
    """ Function called when the 'html parse' command is set in the argument."""
    html_dir = conv_abs(args.html)
    corpus_dir = conv_abs(args.corpus)

    parse.run(html_dir, corpus_dir)

def f_corpus_generate(args):
    """ Function called when the 'corpus generate' command is set in the argument."""
    corpus_dir = conv_abs(args.corpus)

    generate.run(corpus_dir)

def f_corpus_compile(args):
    """ Function called when the 'corpus compile' command is set in the argument."""
    corpus_dir = conv_abs(args.corpus)
    data_dir = conv_abs(args.data)
    # print(corpus_dir, data_dir)

    compile.run(corpus_dir, data_dir)

def add_arguments(parser):
    """Build ArgumentParser."""

    # Help descriptions
    help_aplac = "Execute all the required and complite commands to build up NMT data set for APLaC-Chat."
    help_html = "Command various operations for HTML files."
    help_html_clean = "Clean HTML files by eliminating garbage files and also check if all files are valid and readable."
    help_html_parse = "Parse HTML files and generate corpus files."
    help_corpus = "Command various operations for corpus files."
    help_corpus_generate = "Generate corpus files."
    help_corpus_compile = "Read corpus files and generate the NMT data set (src/tgt/vocab)."

    help_path_html = "HTML files to parse. Absolute or relative path to a directory that contains HTML files, or a single HTML file."
    help_path_corpus = "Corpus files processed during build. Absolute or relative path to a directory where the corpus files are generated and read from."
    help_path_data = "Data files (src/tgt/vocab) generated as outcome. Absolute or relative path to a directory where the data files are generated."

    subparsers = parser.add_subparsers(help="Choose command from below.", dest='command')

    # create the parser for the 'aplac' command
    parser_all = subparsers.add_parser('aplac', help=help_aplac)
    parser_all.add_argument('html', type=str, help=help_path_html)
    parser_all.add_argument('corpus', type=str, help=help_path_corpus)
    parser_all.add_argument('data', type=str, help=help_path_data)
    parser_all.set_defaults(func = f_aplac)

    # create the parser for the 'html' command
    parser_html = subparsers.add_parser('html', help=help_html)
    html_subparsers = parser_html.add_subparsers(help="Choose command from below.")
    # 'html clean' sub-command
    parser_html_clean = html_subparsers.add_parser('clean', help=help_html_clean)
    parser_html_clean.add_argument('html', type=str, help=help_path_html)
    parser_html_clean.set_defaults(func = f_html_clean)
    # 'html parse' sub-command
    parser_html_parse = html_subparsers.add_parser('parse', help=help_html_parse)
    parser_html_parse.add_argument('html', type=str, help=help_path_html)
    parser_html_parse.add_argument('corpus', type=str, help=help_path_corpus)
    parser_html_parse.set_defaults(func = f_html_parse)

    # create the parser for the 'corpus' command
    parser_corpus = subparsers.add_parser('corpus', help=help_corpus)
    corpus_subparsers = parser_corpus.add_subparsers(help="Choose command from below.")
    # 'corpus generate' sub-command
    parser_corpus_generate = corpus_subparsers.add_parser('generate', help=help_corpus_generate)
    parser_corpus_generate.add_argument('corpus', type=str, help=help_path_corpus)
    parser_corpus_generate.set_defaults(func = f_corpus_generate)
    # 'corpus compile' sub-command
    parser_corpus_compile = corpus_subparsers.add_parser('compile', help=help_corpus_compile)
    parser_corpus_compile.add_argument('corpus', type=str, help=help_path_corpus)
    parser_corpus_compile.add_argument('data', type=str, help=help_path_data)
    parser_corpus_compile.set_defaults(func = f_corpus_compile)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    add_arguments(arg_parser)
    args = arg_parser.parse_args()
    args.func(args)     # func is a function pointer which is set for each command with set_defaults function.

    print ("Finished.")