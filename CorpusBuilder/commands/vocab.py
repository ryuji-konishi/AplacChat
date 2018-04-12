# -*- coding: utf-8 -*-
import os
import numpy as np

import resources.loader as ld
import utils.vocab_utils as vocab_utils

# Unocode code page ranges. Note that they are not UTF8, nor UTF16, but code page values.
# https://ja.wikipedia.org/wiki/Unicode%E4%B8%80%E8%A6%A7_3000-3FFF
ascii_ranges = [range(0x0021, 0x007E), range(0x00A1, 0x00FF)]
jpn_symbol_ranges = [range(0x3001, 0x3036), range(0x3099, 0x309E)]
hiragana_ranges = [range(0x3041, 0x3094), range(0x3099, 0x309E)]
katakana_ranges = [range(0x30A1, 0x30F6), range(0x30FB, 0x30FE)]

def _get_code_ranges(code_ranges, words):
    for rng in code_ranges:
        for code in rng:
            words.append(chr(code))

def _generate_standard(file_path):
    """ Generate the starndard vocaburary file for NMT. This vocaburary contains
        the standard charactors:
        - ASCII charactors
        - Commonly used symbols
        - Japanese Hiraganas
        - Japanese Kanjis
        - Japanese Joyo-Kanjis
    """
    words = []

    # Load charactors from Unicode table ranges
    _get_code_ranges(ascii_ranges, words)
    _get_code_ranges(jpn_symbol_ranges, words)
    _get_code_ranges(hiragana_ranges, words)
    _get_code_ranges(katakana_ranges, words)

    # Load Joyo-Kanji from resource
    jk = ld.JoyoKanjiLoader()
    words.extend(jk.load_kanjis())

    # Load Jinmeiyo-Kanji from resource
    jk = ld.JinmeiKanjiLoader()
    words.extend(jk.load_kanjis())

    # Store the loaded characters into VocabStore, then export the vocab file.
    vocab = vocab_utils.VocabStore(file_path)
    vocab.add_vocab_words(words)
    vocab.save_to_file()

def generate(output_dir):
    """ Generate the standard vocaburary file
    """
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    file_path = os.path.join(output_dir, 'vocab.src')
    _generate_standard(file_path)
    print ("Generated:", file_path)

