import sys
sys.path.insert(0, '..\\')  # This is required to import common

sys.setrecursionlimit(2000) # This is to allow bigger sized HTML files. The default is 1000 for Windows.

import os
import utils.file_utils as file_utils
import ParserAtomic as pat
import ParserAtomicHeaderBody as pah
import ParserHeaderBody as phb
import DataStore as ds

html_folder = "C:\\Tmp\\aplac\\html"

current_dir = os.path.dirname(os.path.realpath(__file__))
export_dir = os.path.join(current_dir, 'export')
vocab_file = os.path.join(export_dir, 'vocab.src')
if not os.path.exists(export_dir): os.makedirs(export_dir)

print ("The input directory is", html_folder)
print ("The output directory is", export_dir)

vocab = ds.VocabStore(vocab_file)
result_store = ds.ParseResultStore(vocab)

print ("Searching HTML files in the input directory...")
files = file_utils.get_filelist_in_path("html", html_folder, True)
# files = ["C:\\Tmp\\aplac\\html\\aplac.net\\life\\life53.html"]
# Parse the files and store the result into data store
fileCount = len(files)
print (fileCount, "files to process.")

for idx, f in enumerate(files):
    print ("(", idx, "of", fileCount, ") Processing file", f)
    file_content = file_utils.read_file_any_encoding(f)
    if (len(file_content) == 0):
        continue

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
print ("Exporting the result...")
result_store.export_to_file(export_dir)
vocab.save_to_file()

print ("Finished.")
