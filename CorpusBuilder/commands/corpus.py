import os
import numpy as np
import time

import utils.corpus_utils as corpus_utils
import utils.file_utils as file_utils
import utils.vocab_utils as vocab_utils
import resources.loader as ld
import resources.multiplier as mpl

def generate(output_dir, myname, yourname, pair_loaders, func_validate = None, size_limit_KB = None):
    """ Generate the corpus files from template resources of data.
        The template resources include salute, nodding, themed conversation etc.
        myname is to replace '{myname}' tag appearing in the sentenses. {myname} is 
        a phrase that is used to call yourself, for example, "Hi, my name is {myname}."
        yourname is to replace '{yourname}' tag appearing in the sentenses. {yourname} is 
        a phrase that is used when someone calls you, for example, "Hi {yourname}, nice to see you."
        pair_loaders is a list containing sentense pair resource loaders. Sentense pair resouces are
        a bunch of source/target text pairs that are used to generate corpus data.
        func_validate is a function that takes source/target text pairs from HTML parsers, and it
        returns the validated and cleaned texts. The validated texts are only stored into corpus.
        If omitted any texts will be stored.
        size_limit_KB is the limit of each corpus file to export. The size is in Kilo bite (1024 bytes).
        If the size exceeds the limit, the corpus data is devided and multiple files are exported.
    """
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    corpus_store = corpus_utils.CorpusStore(func_validate = func_validate)
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

    for pair_loader in pair_loaders:
        pairs = pair_loader.load()
        print (len(pairs), "of pairs to process...")
        process(pairs)

    print ("Exporting corpus...")
    exported_files = corpus_store.export_corpus(output_dir, size_limit_KB = size_limit_KB)
    corpus_store.print_report()
    print ("Exported:", exported_files)

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

    # Store the compilation details into log file.
    with open(os.path.join(output_dir, 'compile.log'), 'w') as lf:
        def log_print(*arg):
            """ Log print function. """
            texts = [str(elem) for elem in arg]
            log = ' '.join(texts)
            print(log)
            timeString  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            lf.write("{0} {1}\n".format(timeString, log))
            
        if os.path.isfile(input_path):
            log_print("The input file is", input_path)
            log_print("The vocab file is", vocab_path)
            log_print("The output directory is", output_dir)
            files = [[input_path, os.path.basename(input_path)]]
        else:
            input_dir = input_path
            log_print("The input directory is", input_dir)
            log_print("The vocab file is", vocab_path)
            log_print("The output directory is", output_dir)
            log_print("Searching corpus files in the input directory...")
            files = file_utils.get_filelist_in_path("cor", input_dir, True)

        vocab = vocab_utils.VocabStore(vocab_path)
        corpus_store = corpus_utils.CorpusStore(vocab)
        log_print("Total", len(files), "files to process. Loading...")
        for idx, file in enumerate(files):
            f_abst = file[0]    # absolute path
            f_rel = file[1]     # relative path
            log_print("(", idx, "of", len(files), ") file", f_rel)
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
            log_print("Exporting the", subject, "data into file...")
            corpus_store.export_to_file(output_dir, subject, size_limit_KB, True)
            corpus_store.print_report(log_print)

        # Generate each file set
        process(train, "train")
        process(dev, "dev", 100)
        process(test, "test", 100)

        # Generate vocaburary file that contains words detected in all 3 file lists.
        vocab.sort_by_unicode()
        vocab.save_to_file()
        vocab.print_report(log_print)
        vocab.save_unicode_list(vocab_path + '.txt')

