import os
import uuid
import utils.file_utils as file_utils
import utils.utils as utils
from common import tokenizer as tk
from common import char_utils as cu


special_tokens = tk.special_tokens

class VocabStore(object):
    def __init__(self, vocab_file = None):
        """ If vocab_file is given, read and initialize data from it."""
        self.words_ext = []      # Current existing words in the vocab file.
        self.words_new = []      # New words to be added to the vocab file.
        self.vocab_file = vocab_file
        self.reset_report()
        if vocab_file:
            if os.path.exists(vocab_file):
                vocab, _ = file_utils.read_filelist_any_encoding(vocab_file)
                sp_cnt = len(special_tokens)
                # Vocab files are supposed to contain special tokens at the beginning of file.
                # Verify if the vocab starts with special tokens. Check if the first several elements contains the special tokens.
                if set(vocab[:sp_cnt]).issuperset(special_tokens):
                    # If the existing vocab file is all good, get the vocab into the 
                    # buffer except special tokens.
                    self.words_ext = vocab[sp_cnt:]
                else:
                    # If not, remove the existing file so that a new file will be generated.
                    os.remove(vocab_file)

    def reset_report(self):
        self.export_num = 0
        self.export_appended = False

    def print_report(self, func_print = None):
        if not func_print:
            func_print = print

        if self.export_num > 0:
            if self.export_appended:
                func_print("Vocaburary file is updated with", self.export_num, "of newly added words.")
            else:
                func_print("New vocaburary file is generated.")
        else:
            func_print("No vocaburaries are newly added.")
        func_print("Vocaburaries are now in total of", len(self.words_ext) + len(self.words_new))

    def add_vocab_words(self, words):
        """ Add new vocaburary of list of word"""
        for word in words:
            word = word.strip()
            if word:
                self.add_vocab_word(word)

    def add_vocab_word(self, word):
        """ Add new vocaburary of single word.
            If the word contains none-charctor code it won't be added.
        """
        # If it's a special token, it'll be separatelly processed during saving file. Skip here.
        if word in special_tokens:
            return
        # Check each character in the word. We don't want none-character (control code) in the vocaburary.
        for char in word:
            if cu.is_none_char(char):
                return
        # If it's a new word, store it.
        if (not word in self.words_ext) and (not word in self.words_new):
            self.words_new.append(word)

    def sort_by_unicode(self):
        """ Sort the vocab data by Unicode code point value. """
        utils.sort_unicode_word_list(self.words_new)

    def save_to_file(self, vocab_file = None):
        """ The vocab file is appended with new set of data. 
            The details of vocab file being saved is printed by print_report function separatelly.
        """
        if len(self.words_new) > 0:
            # Use file path which is given either by the constructor or this method's argument.
            # This method's argument takes priority.
            if not vocab_file:
                vocab_file = self.vocab_file

            if vocab_file:
                self.export_appended = False
                if os.path.exists(vocab_file):
                    # Append the data to the existing vocab file.
                    self.export_appended = True
                else:
                    # If the vocab file is to be newly created, initialize the file with special tokens first.
                    with open(vocab_file, 'w', encoding='utf8') as fp:
                        for d in special_tokens:
                            fp.write("%s\n" % d)

                # Append the newly added data
                with open(vocab_file, 'a', encoding='utf8') as fp:
                    for d in self.words_new:
                        fp.write("%s\n" % d)
                        self.export_num += 1

    def save_unicode_list(self, file_path):
        """ For debugging and analysis purposes. Save the vocab words' unicode point value to file. """
        if os.path.exists(file_path):
            os.remove(file_path)

        with open(file_path, 'w', encoding='utf8') as fp:
            for d in special_tokens:
                fp.write("%s\n" % d)

        with open(file_path, 'a', encoding='utf8') as fp:
            for d in self.words_new:
                line = ''
                for c in d:
                    line += "{0:#0{1}x} ".format(ord(c), 6)
                fp.write("%s\n" % line)
