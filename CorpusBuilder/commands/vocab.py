# -*- coding: utf-8 -*-
import os
import numpy as np

import resources.loader as ld
import utils.vocab_utils as vocab_utils

def _generate_standard(file_path):
    """ Generate the starndard vocaburary file for NMT. This vocaburary contains
        the standard charactors:
        - ASCII charactors
        - Commonly used symbols
        - Japanese Hiraganas
        - Japanese Kanjis
        - Japanese Joyo-Kanjis
    """
    # Store the loaded characters into VocabStore, then export the vocab file.
    vocab = vocab_utils.VocabStore(file_path)

    # Load charactors from Unicode table ranges
    vocab.add_vocab_words(vocab_utils.get_charactors_ascii())
    vocab.add_vocab_words(vocab_utils.get_charactors_full_symbol())
    vocab.add_vocab_words(vocab_utils.get_charactors_hiragana())
    vocab.add_vocab_words(vocab_utils.get_charactors_katakana())

    # Load Joyo-Kanji from resource
    jk = ld.JoyoKanjiLoader()
    vocab.add_vocab_words(jk.load())

    # Load Jinmeiyo-Kanji from resource
    jk = ld.JinmeiKanjiLoader()
    vocab.add_vocab_words(jk.load())

    vocab.save_to_file()

def generate(output_dir):
    """ Generate the standard vocaburary file
    """
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    file_path = os.path.join(output_dir, 'vocab.src')
    _generate_standard(file_path)
    print ("Generated:", file_path)

