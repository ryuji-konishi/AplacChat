import os
import uuid
import json
import random
from common import tokenizer as tk
from common import utils

class CorpusStore(object):
    def __init__(self, vocab_store = None, tokenizer = None, func_validate = None):
        """ vocab_store is an instance of VocabStore class.
            tokenizer is an instance of common.tokenizer class.
            func_validate is a function that takes two texts as source and target, and
            return the validated and cleaned texts.
            If omitted any texts will be stored.
        """
        self.data = []
        self.vocab_store = vocab_store
        self.tokenizer = tokenizer
        if not self.tokenizer:
            self.tokenizer = tk.tokenizer()
        self.func_validate = func_validate
        self.reset_report()

    def _copy_data(self, data):
        self.data = data

    def _store_data(self, source_text_line, target_text_line, store_vocab = True):
        is_valid = False
        if self.func_validate:
            # Validate and clean the texts
            source_text_line, target_text_line = self.func_validate(source_text_line, target_text_line)
            if source_text_line and target_text_line:
                is_valid = True
        else:
            is_valid = True

        if is_valid:
            self.data.append([source_text_line, target_text_line])
            if self.vocab_store and store_vocab:
                buf_list = self.tokenizer.split(source_text_line)
                self.vocab_store.add_vocab_words(buf_list)
                buf_list = self.tokenizer.split(target_text_line)
                self.vocab_store.add_vocab_words(buf_list)

    def reset_report(self):
        self.export_num = 0

    def print_report(self, func_print = None):
        if not func_print:
            func_print = print

        if self.export_num > 0:
            func_print("CorpusStore exported", self.export_num, "of sentenses.")
        else:
            func_print("No sentenses are exported.")

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
            new_instance = CorpusStore(self.vocab_store, self.tokenizer, self.func_validate)
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
        for src, tgt in zip(source, target):
            self._store_data(src, tgt)

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

                self.export_num += 1

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
