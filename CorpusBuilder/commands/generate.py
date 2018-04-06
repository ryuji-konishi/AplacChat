import os

import numpy as np
import utils.DataStore as ds
import utils.file_utils as file_utils

def run(output_dir):
    """ Generate the corpus files
    """
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    corpus_store = ds.CorpusStore()

    dev = np.array([
        ['ども、アキラです', 'アキラさん、こんにちは'],
        ['ども、Ryujiです', 'Ryujiさん、こんにちは']
    ])
    src = dev[:, 0]
    tgt = dev[:, 1]
    corpus_store.store_data(src, tgt)
    output_path = corpus_store.export_corpus(output_dir)
    print ("Exported:", output_path)

