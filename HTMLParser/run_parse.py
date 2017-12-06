import sys
sys.path.insert(0, '..\\')  # This is required to import common

import os
import utils.file_utils as file_utils
import ParserAtomic as pat
import ParserAtomicHeaderBody as pah
import ParserHeaderBody as phb
import DataStore as ds

html_folder = "C:\\Tmp\\aplac\\html"

current_dir = os.path.dirname(os.path.realpath(__file__))
export_dir = os.path.join(current_dir, 'export')
vocab_file = os.path.join(current_dir, 'vocab.src')
if not os.path.exists(export_dir): os.makedirs(export_dir)

vocab = ds.VocabStore(vocab_file)
result_store = ds.ParseResultStore(vocab)
files = file_utils.get_filelist_in_path("html", html_folder, False)
# Parse the files and store the result into data store
for f in files:
    file_content = file_utils.read_file_any_encoding(f)

    # 1st, process the data with Atomic Parser
    parser = pat.Parser(result_store)
    parser.parse(file_content)

    # Process the same data with Atomic HeaderBody Parser
    parser = pah.Parser(result_store)
    parser.parse(file_content)

    # Process the same data with HeaderBody Parser
    parser = phb.Parser(result_store)
    parser.parse(file_content)

# Export the parsed data into file
result_store.export_to_file(export_dir)
vocab.save_to_file()
