import sys
sys.path.insert(0, '..\\')  # This is required to import common
sys.setrecursionlimit(2000) # This is to allow more recursive function calls for bigger sized HTML files. The default is 1000 for Windows.

import os
import argparse
import utils.file_utils as file_utils
import utils.utils as utils
import utils.DataStore as ds
import parsers.ParserAtomic as pat
import parsers.ParserAtomicHeaderBody as pah
import parsers.ParserHeaderBody as phb

def corpus(input_path, export_dir):
    """ Compile the corpus files and generate a set of NMT data files (train/dev/test).
        input_path is either a folder path or file path, both in absolute path.
    """
    vocab_file = os.path.join(export_dir, 'vocab.src')
    if not os.path.exists(export_dir): os.makedirs(export_dir)
    vocab = ds.VocabStore(vocab_file)

    if os.path.isfile(input_path):
        print ("The input file is", input_path)
        print ("The output directory is", export_dir)
        files = [[input_path, os.path.basename(input_path)]]
    else:
        input_dir = input_path
        print ("The input directory is", input_dir)
        print ("The output directory is", export_dir)
        print ("Searching corpus files in the input directory...")
        files = file_utils.get_filelist_in_path("cor", input_dir, True)

    corpus_store = ds.CorpusStore(vocab)
    print ("Total", len(files), "files to process. Loading...")
    for idx, file in enumerate(files):
        f_abst = file[0]    # absolute path
        f_rel = file[1]     # relative path
        print ("(", idx, "of", len(files), ") file", f_rel)
        # Import and restore corpus store.
        # Don't restore vocaburary here. It's time consuming. It'll be restored during export later on.
        corpus_store.import_corpus(f_abst, False)

    # Split the corpus data randomly into 3 blocks - train, dev and test.
    # The distribution ratio is train 98%, dev 1% and test 1%.
    # Be careful not to make dev and test files too big otherwise Tensorflow training
    # fails with out-of-memory (even with GPU machine).
    train, dev, test = corpus_store.split((0.98, 0.01, 0.01))

    def process(corpus_store, subject, size_limit_KB = None):
        """ size_limit_KB is the limit of file size to be written. The size is in Kilo bite (1024 bytes)
        """
        # Export the corpus data into file. Also vocaburary is restored here.
        print ("Exporting the", subject, "data into file...")
        corpus_store.export_to_file(export_dir, subject, size_limit_KB, True)

    # Generate each file set
    process(train, "train")
    process(dev, "dev", 100)
    process(test, "test", 100)

    # Generate vocaburary file that contains words detected in all 3 file lists.
    vf = vocab.save_to_file()
    if vf:
        print ("Vocaburary file is updated:", vf)
    else:
        print ("No updates in vocaburary.")

def parse_html(input_path, export_dir):
    """ Parse the HTML files and generate a corpus file.
        input_path is either a folder path or file path, both in absolute path.
    """

    def process(files):
        """ size_limit_KB is the limit of file size to be written. The size is in Kilo bite (1024 bytes)
        """
        corpus_store = ds.CorpusStore()

        for idx, file in enumerate(files):
            f_abst = file[0]    # absolute path
            f_rel = file[1]     # relative path
            print ("(", idx, "of", len(files), ") file", f_rel)
            file_content = file_utils.read_file_any_encoding(f_abst)
            if (len(file_content) == 0):
                continue

            # 1st, process the data with Atomic Parser
            parser = pat.Parser(corpus_store)
            parser.parse(file_content)

            # Process the same data with Atomic HeaderBody Parser
            parser = pah.Parser(corpus_store)
            parser.parse(file_content)

            # Process the same data with HeaderBody Parser
            parser = phb.Parser(corpus_store)
            parser.parse(file_content)

        # Export the parsed data into file
        print ("Exporting the result...")
        return corpus_store.export_corpus(export_dir)

    if os.path.isfile(input_path):
        print ("The input file is", input_path)
        print ("The output directory is", export_dir)
        files = [[input_path, os.path.basename(input_path)]]
    else:
        input_dir = input_path
        print ("The input directory is", input_dir)
        print ("The output directory is", export_dir)
        print ("Searching HTML files in the input directory...")
        files = file_utils.get_filelist_in_path("html", input_dir, True)

    print ("Total", len(files), "files to process.")
    output_path = process(files)
    print ("Exported:", output_path)

def add_arguments(parser):
    """Build ArgumentParser."""
    parser.add_argument("--mode", type=str, default="debug", help="""\
      uni | bi | gnmt. For bi, we build num_layers/2 bi-directional layers.For
      gnmt, we build 1 bi-directional layer, and (num_layers - 1) uni-
      directional layers.\
      """)

if __name__ == "__main__":
    print ('build started.')
    arg_parser = argparse.ArgumentParser()
    add_arguments(arg_parser)
    args = arg_parser.parse_args()
    
    if args.mode == 'debug':
        input_dir = "C:\\Tmp\\aplac\\data\\xs"
        export_dir = "C:\\Tmp\\aplac\\data\\xs"
        corpus(input_dir, export_dir)
    elif args.mode == 'parse':
        # input_dir = "C:\\Tmp\\aplac\\html\\aplac.net"
        input_dir = "C:\\Tmp\\aplac\\html\\xs"
        # current_dir = os.path.dirname(os.path.realpath(__file__))
        # export_dir = os.path.join(current_dir, 'export')
        export_dir = "C:\\Tmp\\aplac\\data\\xs"
        parse_html(input_dir, export_dir)
    else:
        print (args.mode)

print ("Finished.")
