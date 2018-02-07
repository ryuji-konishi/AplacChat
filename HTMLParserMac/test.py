import sys
# Windows
# sys.path.insert(0, '..\\')  # This is required to import common
# Mac/Linux
sys.path.insert(0, '..//')  # This is required to import common

import os
import utils.file_utils as file_utils
import ParserAtomic as pat
import DataStore as ds

html_folder = "C:\\Tmp\\tensorflow\\nmt\\aplac_html"

current_dir = os.path.dirname(os.path.realpath(__file__))
export_dir = os.path.join(current_dir, 'export')
vocab_file = os.path.join(current_dir, 'vocab.txt')
if not os.path.exists(export_dir): os.makedirs(export_dir)

vocab = ds.VocabStore(vocab_file)
result_store = ds.ParseResultStore(vocab)
files = file_utils.get_filelist_in_path("html", html_folder, False)

for f in files:
    file_content = file_utils.read_file_any_encoding(f)

    parser = pat.Parser(result_store)
    parser.parse(file_content)

