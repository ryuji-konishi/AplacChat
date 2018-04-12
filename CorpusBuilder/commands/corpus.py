import os

import numpy as np
import utils.corpus_utils as corpus_utils
import utils.file_utils as file_utils
import utils.vocab_utils as vocab_utils
import resources.loader as ld
import resources.multiplier as mpl

def generate(output_dir, myname = '田村', yourname = '田村さん'):
    """ Generate the corpus files from template resources of data.
        The template resources include salute, nodding, themed conversation etc.
    """
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    corpus_store = corpus_utils.CorpusStore()
    def process(pairs):
        """ Loop through the list of src/tgt pairs, replace the resource tags (name, city etc)
            and store the result into CorpusStore.
        """
        multipliers = [mpl.NameMultiplier(), mpl.CityMultiplier(), mpl.CountryMultiplier(), 
            mpl.LocationMultiplier(), mpl.ThingMultiplier()]
        for src, tgt in pairs:
            src = src.replace('{myname}', myname)
            tgt = tgt.replace('{myname}', myname)
            src = src.replace('{yourname}', yourname)
            tgt = tgt.replace('{yourname}', yourname)

            srcs = [src]
            tgts = [tgt]

            for multiplier in multipliers:
                srcs, tgts = multiplier.multiply(srcs, tgts)
            corpus_store.store_data(srcs, tgts)

    # Process salute sentences
    sl = ld.SaluteLoader()
    salutes = sl.load_salutes()
    print (len(salutes), "of salute sentenses to process...")
    process(salutes)
    
    # Process conversation sentences
    cl = ld.ConversationLoader()
    convs = cl.load_conversations()
    print (len(convs), "of conversation sentenses to process...")
    process(convs)
    
    print ("Exporting corpus...")
    output_path = corpus_store.export_corpus(output_dir)
    print ("Exported:", output_path)

def compile(input_path, vocab_path, output_dir):
    """ Compile the corpus files and generate a set of NMT data files (train/dev/test).
        input_path is the corpus data, either a folder path or file path, both in absolute path.
        vocab_path is the vocaburary file, either a folder path or file path, both in absolute path. 
        If folder path is given, the file name defaults 'vocab.src'.
        output_dir is the path to the folder where the data set is generated.
    """
    # Create output directory if not exist
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    
    # Create vocab file directory if not exist. And get the file path.
    if not os.path.isfile(vocab_path):
        if not os.path.exists(vocab_path): os.makedirs(vocab_path)
        vocab_path = os.path.join(vocab_path, 'vocab.src')

    if os.path.isfile(input_path):
        print ("The input file is", input_path)
        print ("The vocab file is", vocab_path)
        print ("The output directory is", output_dir)
        files = [[input_path, os.path.basename(input_path)]]
    else:
        input_dir = input_path
        print ("The input directory is", input_dir)
        print ("The vocab file is", vocab_path)
        print ("The output directory is", output_dir)
        print ("Searching corpus files in the input directory...")
        files = file_utils.get_filelist_in_path("cor", input_dir, True)

    vocab = vocab_utils.VocabStore(vocab_path)
    corpus_store = corpus_utils.CorpusStore(vocab)
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
    train, dev, test = corpus_store.split_rnd((0.98, 0.01, 0.01))

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
    updated = vocab.save_to_file()
    if updated:
        print ("Vocaburary file is updated.")
        vocab.print_report()
    else:
        print ("No updates in vocaburary.")

