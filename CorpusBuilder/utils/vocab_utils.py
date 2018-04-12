import os
import utils.file_utils as file_utils
from common import tokenizer as tk

special_tokens = tk.special_tokens

class VocabStore(object):
    def __init__(self, vocab_file = None):
        """ If vocab_file is given, read and initialize data from it."""
        self.data_ext = list(special_tokens)      # Current existing data in the vocab file.
        self.data_new = list(special_tokens)      # New data to be added to the vocab file.
        self.vocab_file = vocab_file
        self.reset_report()
        if vocab_file:
            if os.path.exists(vocab_file):
                vocab = file_utils.read_filelist_any_encoding(vocab_file)
                sp_cnt = len(special_tokens)
                # Verify if the vocab starts with special tokens. Check if the first several elements contains the special tokens.
                if set(vocab[:sp_cnt]).issuperset(special_tokens):
                    # IF the existing vocab file is all good, get the vocab into the 
                    # buffer, and clear the data_new so that only newly added vocab words
                    # will be appended into the existing file.
                    self.data_ext = vocab
                    self.data_new = []
                else:
                    # If not, remove the existing file so that a new file will be generated.
                    os.remove(vocab_file)

    def reset_report(self):
        self.word_num = 0

    def print_report(self):
        if self.word_num > 0:
            print("Vocaburary file is updated with", self.word_num, "of words newly added.")
        else:
            print("Nothing to report.")

    def add_vocab_words(self, words):
        """ Add new vocaburary of list of word"""
        for w in words:
            w = w.strip()
            if w:
                if (not w in self.data_ext) and (not w in self.data_new):
                    self.data_new.append(w)

    def save_to_file(self, vocab_file = None):
        """ The vocab file is appended with new set of data. 
            Return True when the file is updated. Otherwise return False. 
        """
        result = False
        if len(self.data_new) > 0:
            # Use file path which is given either by the constructor or this method's argument.
            # This method's argument takes priority.
            if not vocab_file:
                vocab_file = self.vocab_file

            if vocab_file:
                f = open(self.vocab_file, 'a', encoding='utf8')
                for d in self.data_new:
                    f.write("%s\n" % d)
                    self.word_num += 1
                f.close()
                result = True
        return result
