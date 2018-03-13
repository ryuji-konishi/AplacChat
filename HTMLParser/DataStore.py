import os
import uuid
import utils.file_utils as file_utils
from common import vocab

special_tokens = vocab.special_tokens

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

    def __init__(self, vocab_store):
        self.data = []
        self.vocab_store = vocab_store

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

            buf_list = vocab.delimit_multi_char_text(source_text_line)
            self.vocab_store.add_vocab_words(buf_list)
            buf_str = vocab.join_list_by_space(buf_list)
            src += buf_str + '\n'

            buf_list = vocab.delimit_multi_char_text(target_text_line)
            self.vocab_store.add_vocab_words(buf_list)
            buf_str = vocab.join_list_by_space(buf_list)
            tgt += buf_str + '\n'

        # src = trim_structural_char(src)
        # tgt = trim_structural_char(tgt)
        self.data.append([src, tgt])

    def export_to_file(self, out_dir):
        basename = str(uuid.uuid4())
        src_file = basename + '.src'
        tgt_file = basename + '.tgt'
        sf = open(os.path.join(out_dir, src_file), 'w', encoding='utf8')
        tf = open(os.path.join(out_dir, tgt_file), 'w', encoding='utf8')
        for d in self.data:
            source_lines, target_lines = d[0], d[1]
            # self.export_src_tgt_file(out_dir, d[0], d[1])
            sf.write(source_lines)
            tf.write(target_lines)
        sf.close()
        tf.close()

    def export_src_tgt_file(self, out_dir, source_lines, target_lines):
        basename = str(uuid.uuid4())
        src_file = basename + '.src'
        tgt_file = basename + '.tgt'
        f = open(os.path.join(out_dir, src_file), 'w', encoding='utf8')
        f.write(source_lines)
        f.close()
        f = open(os.path.join(out_dir, tgt_file), 'w', encoding='utf8')
        f.write(target_lines)
        f.close()

