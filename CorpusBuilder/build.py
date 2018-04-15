import sys
sys.path.insert(0, '..\\')  # This is required to import common

import os
import argparse
import time
import commands.html as html
import commands.corpus as corpus
import commands.vocab as vocab
import aplac.aplac as aplac

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

    args.__dict__['vocab'] = args.data       # Generate the standard vocab.src file as the base at the data directory.

    f_html_clean(args)
    f_html_parse(args)
    f_vocab_generate(args)       
    f_corpus_generate(args)
    f_corpus_compile(args)

def f_html_clean(args):
    """ Function called when the 'html clean' command is set in the argument."""
    html_dir = conv_abs(args.html)

    html.clean(html_dir)

def f_html_parse(args):
    """ Function called when the 'html parse' command is set in the argument."""
    html_dir = conv_abs(args.html)
    corpus_dir = conv_abs(args.corpus)

    # APLaC specific
    html.parse(html_dir, corpus_dir, aplac.validate_pair_html, aplac.html_target_tag)

def f_corpus_generate(args):
    """ Function called when the 'corpus generate' command is set in the argument."""
    corpus_dir = conv_abs(args.corpus)

    # APLaC specific
    pair_loaders = [aplac.SaluteLoader(), aplac.ConversationLoader()]
    corpus.generate(corpus_dir, aplac.myname, aplac.yourname, pair_loaders, aplac.validate_pair_corpus)

def f_corpus_compile(args):
    """ Function called when the 'corpus compile' command is set in the argument."""
    corpus_dir = conv_abs(args.corpus)
    vocab_path = conv_abs(args.vocab)
    data_dir = conv_abs(args.data)

    corpus.compile(corpus_dir, vocab_path, data_dir)

def f_vocab_generate(args):
    """ Function called when the 'vocab generate' command is set in the argument."""
    vocab_dir = conv_abs(args.vocab)

    vocab.generate(vocab_dir)

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
    help_vocab = "Command various operations for vocab files."
    help_vocab_generate = "Generate the standard vocab file."

    help_path_html = "HTML files to parse. Absolute or relative path to a directory that contains HTML files, or a single HTML file."
    help_path_corpus = "Corpus files processed during build. Absolute or relative path to a directory where the corpus files are generated and read from."
    help_path_data = "Data files (src/tgt/vocab) generated as outcome. Absolute or relative path to a directory where the data files are generated."
    help_path_vocab = "Vocaburary file (vocab) processed during build. Absolute or relative path to a directory where the file is generated."

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
    parser_corpus_compile.add_argument('vocab', type=str, help=help_path_vocab)
    parser_corpus_compile.add_argument('data', type=str, help=help_path_data)
    parser_corpus_compile.set_defaults(func = f_corpus_compile)

    # create the parser for the 'vocab' command
    parser_vocab = subparsers.add_parser('vocab', help=help_vocab)
    vocab_subparsers = parser_vocab.add_subparsers(help="Choose command from below.")
    # 'vocab generate' sub-command
    parser_vocab_generate = vocab_subparsers.add_parser('generate', help=help_vocab_generate)
    parser_vocab_generate.add_argument('vocab', type=str, help=help_path_vocab)
    parser_vocab_generate.set_defaults(func = f_vocab_generate)

def main():
    arg_parser = argparse.ArgumentParser()
    add_arguments(arg_parser)
    args = arg_parser.parse_args()
    if 'func' in args:
        st = time.time()
        args.func(args)     # func is a function pointer which is set for each command with set_defaults function.
        ts = time.time() - st   # time spent
        if ts > 6000:
            print ("Time", round(ts / 3600, 2), "hour")
        elif ts > 100:
            print ("Time", round(ts / 60, 2), "min")
        else:
            print ("Time", round(ts, 2), "sec")
    else:
        print("But. ArgumentParser is not correctly configured.")   # You can't reach here.

if __name__ == "__main__":
    main()
        
    # class Namespace:
    #     def __init__(self, **kwargs):
    #         self.__dict__.update(kwargs)    
    # args = Namespace(html = "C:\\Tmp\\aplac\\html\\xs", corpus ="C:\\Tmp\\aplac\\corpus\\test", 
    #     data ="C:\\Tmp\\aplac\\data\\xs", vocab = "C:\\Tmp\\aplac\\data\\test")
    # f_vocab_generate(args)

    print ("Finished.")
