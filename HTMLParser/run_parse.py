import sys
sys.path.insert(0, '..\\')  # This is required to import common

sys.setrecursionlimit(2000) # This is to allow bigger sized HTML files. The default is 1000 for Windows.

import os
import utils.file_utils as file_utils
import utils.utils as utils
import ParserAtomic as pat
import ParserAtomicHeaderBody as pah
import ParserHeaderBody as phb
import DataStore as ds

# Parse the files and store the result into data store


html_folder = "C:\\Tmp\\aplac\\html\\aplac.net"
# html_folder = "C:\\Tmp\\aplac\\html\\xs"

# current_dir = os.path.dirname(os.path.realpath(__file__))
# export_dir = os.path.join(current_dir, 'export')
export_dir = "C:\\Tmp\\aplac\\data\\xs"
vocab_file = os.path.join(export_dir, 'vocab.src')
if not os.path.exists(export_dir): os.makedirs(export_dir)

print ("The input directory is", html_folder)
print ("The output directory is", export_dir)

vocab = ds.VocabStore(vocab_file)

print ("Searching HTML files in the input directory...")
files = file_utils.get_filelist_in_path("html", html_folder, True)
# Distribute the list of files randomly into 3 lists - train, dev and test.
# The distribution ratio is train 98%, dev 1% and test 1%.
# Be careful not to make dev and test files too big otherwise Tensorflow training
# fails with out-of-memory (even with GPU machine).
trains, devs, tests = utils.distribute_rnd(files, (0.98, 0.01, 0.01))

# trains = [("C:\\Tmp\\aplac\\html\\aplac.net\\life\\life53.html", "life\\life53.html")]
# devs = [("C:\\Tmp\\aplac\\html\\aplac.net\\life\\life53.html", "life\\life53.html")]
# tests = [("C:\\Tmp\\aplac\\html\\aplac.net\\life\\life53.html", "life\\life53.html")]


def process(files, subject, vocab_store, size_limit_KB = None):
    """ size_limit_KB is the limit of file size to be written. The size is in Kilo bite (1024 bytes)
    """
    result_store = ds.ParseResultStore(vocab_store)

    for idx, file in enumerate(files):
        f_abst = file[0]    # absolute path
        f_rel = file[1]     # relative path
        print (subject, "(", idx, "of", len(files), ") file", f_rel)
        file_content = file_utils.read_file_any_encoding(f_abst)
        if (len(file_content) == 0):
            continue

        # 1st, process the data with Atomic Parser
        parser = pat.Parser(result_store)
        parser.parse(file_content)

        # Process the same data with Atomic HeaderBody Parser
        parser = pah.Parser(result_store)
        parser.parse(file_content)

        # Process the same data with HeaderBody Parser
        parser = phb.Parser(result_store)
        parser.parse(file_content)

    # Export the parsed data into file
    print ("Exporting the result...")
    result_store.export_to_file(export_dir, subject, size_limit_KB)

# Generate each file set
print ("Total", len(files), "files to process.")
process(trains, "train", vocab)
process(devs, "dev", vocab, 100)
process(tests, "test", vocab, 100)

# Generate vocaburary file that contains words detected in all 3 file lists.
vocab.save_to_file()

print ("Finished.")
