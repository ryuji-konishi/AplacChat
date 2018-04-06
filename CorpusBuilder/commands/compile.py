import os

import utils.file_utils as file_utils
import utils.DataStore as ds

def run(input_path, output_dir):
    """ Compile the corpus files and generate a set of NMT data files (train/dev/test).
        input_path is either a folder path or file path, both in absolute path.
    """
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    if os.path.isfile(input_path):
        print ("The input file is", input_path)
        print ("The output directory is", output_dir)
        files = [[input_path, os.path.basename(input_path)]]
    else:
        input_dir = input_path
        print ("The input directory is", input_dir)
        print ("The output directory is", output_dir)
        print ("Searching corpus files in the input directory...")
        files = file_utils.get_filelist_in_path("cor", input_dir, True)

    vocab_file = os.path.join(output_dir, 'vocab.src')
    vocab = ds.VocabStore(vocab_file)
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
        corpus_store.export_to_file(output_dir, subject, size_limit_KB, True)

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
