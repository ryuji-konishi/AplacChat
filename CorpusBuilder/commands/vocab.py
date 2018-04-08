import os

import numpy as np
import utils.file_utils as file_utils
import utils.vocab_utils as vocab_utils


def generate(output_dir):
    """ Generate the standard vocaburary file
    """
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    file_path = os.path.join(output_dir, 'vocab.src')
    vocab_utils.generate_standard_vocaburary(file_path)
    print ("Generated:", file_path)

