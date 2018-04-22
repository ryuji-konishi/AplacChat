# -*- coding: utf-8 -*-
import os
import numpy as np

import resources.loader as ld
import utils.vocab_utils as vocab_utils
from common import char_utils as cu

def _add_standard_words(vocab):
    """ Add the starndard vocaburary words. The standard words are:
        - ASCII charactors
        - Commonly used symbols
        - Japanese Hiraganas
        - Japanese Kanjis
        - Japanese Joyo-Kanjis
    """
    # Load charactors from Unicode table ranges
    vocab.add_vocab_words(cu.get_chars_ascii())
    vocab.add_vocab_words(cu.get_chars_deco_number())
    vocab.add_vocab_words(cu.get_chars_full_symbol())
    vocab.add_vocab_words(cu.get_chars_full_number())
    vocab.add_vocab_words(cu.get_chars_full_alphabet())
    vocab.add_vocab_words(cu.get_chars_hiragana())
    vocab.add_vocab_words(cu.get_chars_katakana())
    vocab.add_vocab_words(cu.get_chars_katakana_half())

    # Load Joyo-Kanji from resource
    jk = ld.JoyoKanjiLoader()
    vocab.add_vocab_words(jk.load())

    # Load Jinmeiyo-Kanji from resource
    jk = ld.JinmeiKanjiLoader()
    vocab.add_vocab_words(jk.load())

def generate(output_dir):
    """ Generate the standard vocaburary file
    """
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    file_path = os.path.join(output_dir, 'vocab.src')
    # Store the loaded characters into VocabStore, then export the vocab file.
    vocab = vocab_utils.VocabStore(file_path)
    _add_standard_words(vocab)
    vocab.sort_by_unicode()
    vocab.save_to_file()
    vocab.print_report()
    # For analysis purposes, export in unicode code point.
    vocab.save_unicode_list(file_path + '.txt')

