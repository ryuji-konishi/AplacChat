import os
import uuid
import json
import utils.file_utils as file_utils
from common import SentenseResolver as sr
from common import utils

special_tokens = sr.special_tokens

class VocabStore(object):
    def __init__(self, vocab_file = None):
        """ If vocab_file is given, read and initialize data from it."""
        self.data_ext = list(special_tokens)      # Current existing data in the vocab file.
        self.data_new = list(special_tokens)      # New data to be added to the vocab file.
        self.vocab_file = vocab_file
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

    def add_vocab_words(self, words):
        """ Add new vocaburary of list of word"""
        for w in words:
            w = w.strip()
            if w:
                if (not w in self.data_ext) and (not w in self.data_new):
                    self.data_new.append(w)

    def save_to_file(self, vocab_file = None):
        """ The vocab file is appended with new set of data."""
        if len(self.data_new) > 0:
            # Use file path which is given either by the constructor or this method's argument.
            # This method's argument takes priority.
            fp = vocab_file
            if not fp: fp = self.vocab_file

            if fp:
                f = open(self.vocab_file, 'a', encoding='utf8')
                for d in self.data_new:
                    f.write("%s\n" % d)
                f.close()

class ParseResultStore(object):
    # def __init__(self):
    #     self.data = []

    def __init__(self, vocab_store = None):
        self.data = []
        self.vocab_store = vocab_store
        self.resolver = sr.SentenseResolver()

    # def store_result(self, source_text, target_text):
    #     self.data.append([source_text, target_text])

    def clear(self):
        del self.data[:]

    def store_result(self, source, target):
        """ source/target is either a line of text or a list of text.
        This function stores the source/target text line after splitting in 
        character/word level and then concatenated by space ' '.
        Also those charactger/word is added into the vocabulary.
        """
        if len(source) == 0 or len(target) == 0:
            return
        if isinstance(source, str):
            source = [source]
        if isinstance(target, str):
            target = [target]
        src, tgt = '', ''
        for result in zip(source, target):
            source_text_line, target_text_line = result[0], result[1]

            src_list = self.resolver.split(source_text_line)
            buf_str = utils.join_list_by_space(src_list)
            src += buf_str + '\n'

            tgt_list = self.resolver.split(target_text_line)
            buf_str = utils.join_list_by_space(tgt_list)
            tgt += buf_str + '\n'

            if self.vocab_store:
                self.vocab_store.add_vocab_words(src_list)
                self.vocab_store.add_vocab_words(tgt_list)

        # src = trim_structural_char(src)
        # tgt = trim_structural_char(tgt)
        self.data.append([src, tgt])

    def export_to_file(self, out_dir, basename = None, size_limit_KB = None):
        """ Write out the stored source/target data into a pair of src/tgt files.
            basename is the file name exclude extension. If omitted, ramdom name is generated.
            size_limit_KB is the limit of file size to be written. The size is in Kilo bite (1024 bytes)
        """
        if not basename:
            basename = str(uuid.uuid4())
        if size_limit_KB:
            size_limit = size_limit_KB * 1024
        else:
            size_limit = None

        src_path = os.path.join(out_dir, basename + '.src')
        tgt_path = os.path.join(out_dir, basename + '.tgt')
        with open(src_path, 'w', encoding='utf8') as sf, open(tgt_path, 'w', encoding='utf8') as tf:
            for d in self.data:
                source_lines, target_lines = d[0], d[1]
                sf.write(source_lines)
                tf.write(target_lines)
                if size_limit:
                    if sf.tell() > size_limit or tf.tell() > size_limit:
                        break

    def export_corpus(self, out_dir, basename = None, size_limit_KB = None):
        """ Write out the stored source/target data into a corpus file.
            basename is the file name exclude extension. If omitted, ramdom name is generated.
            size_limit_KB is the limit of file size to be written. The size is in Kilo bite (1024 bytes)
            Return the absolute path to the exported file.
        """
        if not basename:
            basename = str(uuid.uuid4())
        if size_limit_KB:
            size_limit = size_limit_KB * 1024
        else:
            size_limit = None

        file_path = os.path.join(out_dir, basename + '.cor')
        with open(file_path, 'w', encoding='utf8') as fn:
            json.dump(self.data, fn, ensure_ascii=False)

        return file_path
