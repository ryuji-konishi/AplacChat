import os
import uuid
import json
import random
import utils.file_utils as file_utils
from common import tokenizer as tk
from common import utils

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

class CorpusStore(object):
    def __init__(self, vocab_store = None, tokenizer = None):
        self.data = []
        self.vocab_store = vocab_store
        self.tokenizer = tokenizer
        if not self.tokenizer:
            self.tokenizer = tk.tokenizer()

    def _copy_data(self, data):
        self.data = data

    def _store_data(self, source_text_line, target_text_line, store_vocab = True):
        self.data.append([source_text_line, target_text_line])
        if self.vocab_store and store_vocab:
            buf_list = self.tokenizer.split(source_text_line)
            self.vocab_store.add_vocab_words(buf_list)
            buf_list = self.tokenizer.split(target_text_line)
            self.vocab_store.add_vocab_words(buf_list)

    def clear(self):
        del self.data[:]

    def split_rnd(self, ratio):
        """ Split the data randomly into multiple blocks. Then each block is contained by another
            instance of self class, and the returned value is the tuple of those instances.
            The ratio is a tuple containing the distribution ratios in float totaling 1.
        """
        random.shuffle(self.data)
        return self.split(ratio)

    def split(self, ratio):
        """ Split the data into multiple blocks. Then each block is contained by another
            instance of self class, and the returned value is the tuple of those instances.
            The ratio is a tuple containing the distribution ratios in float totaling 1.
        """
        if sum(ratio) != 1:
            raise ValueError("The ratio has to add up to 1.")

        result_lists = []
        data_cnt = len(self.data)

        # List of each length of result lists.
        ratio_lens = [int(data_cnt * r) for r in ratio]
        st = 0
        for l in ratio_lens:
            # Create another instance that contains the split data
            split_data = self.data[st:st + l]
            new_instance = CorpusStore(self.vocab_store, self.tokenizer)
            new_instance._copy_data(split_data)
            result_lists.append(new_instance)
            st += l

        return tuple(result_lists)

    def store_data(self, source, target):
        """ source/target is either a line of text or a list of text.
        This function stores the source/target text line into the list
        while splitting the text into character/word level and adding into the vocabulary.
        """
        if len(source) == 0 or len(target) == 0:
            return
        if isinstance(source, str):
            source = [source]
        if isinstance(target, str):
            target = [target]
        for data in zip(source, target):
            source_text_line, target_text_line = data[0], data[1]
            self._store_data(source_text_line, target_text_line)

    def export_to_file(self, out_dir, basename = None, size_limit_KB = None, store_vocab = False):
        """ Write out the stored source/target data into a pair of src/tgt files.
            The text is splitted into character/word level and then concatenated by space ' '.
            basename is the file name exclude extension. If omitted, ramdom name is generated.
            size_limit_KB is the limit of file size to be written. The size is in Kilo bite (1024 bytes)
            When store_vacab is True, the splitted text is stored into vocaburary store. This is useful
            if you want to do the two things, exporting into file and storing into vocaburary, at the 
            same time and improve performance.
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
                source_text_line, target_text_line = d[0], d[1]

                src_list = self.tokenizer.split(source_text_line)
                buf_str = utils.join_list_by_space(src_list)
                sf.write(buf_str + '\n')

                tgt_list = self.tokenizer.split(target_text_line)
                buf_str = utils.join_list_by_space(tgt_list)
                tf.write(buf_str + '\n')

                if self.vocab_store and store_vocab:
                    self.vocab_store.add_vocab_words(src_list)
                    self.vocab_store.add_vocab_words(tgt_list)

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
        with open(file_path, 'w', encoding='utf8') as fp:
            json.dump(self.data, fp, ensure_ascii=False)

        return file_path

    def import_corpus(self, file_path, restore_vocab):
        """ Read the corpus file and restore the data.
            When restore_vacab is True, the vocaburary is also restored.
        """
        with open(file_path, 'r', encoding='utf8') as fp:
            lines = json.load(fp)
            for data in lines:
                source_text_line, target_text_line = data[0], data[1]
                self._store_data(source_text_line, target_text_line, restore_vocab)
