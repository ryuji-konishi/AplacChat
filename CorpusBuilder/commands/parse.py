import sys
sys.setrecursionlimit(2000) # This is to allow more recursive function calls for bigger sized HTML files. The default is 1000 for Windows.

import os

import utils.file_utils as file_utils
import utils.DataStore as ds
import parsers.ParserAtomic as pat
import parsers.ParserAtomicHeaderBody as pah
import parsers.ParserHeaderBody as phb

def run(input_path, output_dir):
    """ Parse the HTML files and generate a corpus file.
        input_path is either a folder path or file path, both in absolute path.
    """
    if not os.path.exists(output_dir): os.makedirs(output_dir)

    if os.path.isfile(input_path):
        print ("The input file is", input_path)
        print ("The output directory is", output_dir)
        files = [[input_path, os.path.basename(input_path)]]
    else:
        input_dir = input_path
        print ("The input directory is", input_dir)
        print ("The output directory is", output_dir)
        print ("Searching HTML files in the input directory...")
        files = file_utils.get_filelist_in_path("html", input_dir, True)

    def process(files):
        """ size_limit_KB is the limit of file size to be written. The size is in Kilo bite (1024 bytes)
        """
        corpus_store = ds.CorpusStore()

        for idx, file in enumerate(files):
            f_abst = file[0]    # absolute path
            f_rel = file[1]     # relative path
            print ("(", idx, "of", len(files), ") file", f_rel)
            file_content = file_utils.read_file_any_encoding(f_abst)
            if (len(file_content) == 0):
                continue

            # 1st, process the data with Atomic Parser
            parser = pat.Parser(corpus_store)
            parser.parse(file_content)

            # Process the same data with Atomic HeaderBody Parser
            parser = pah.Parser(corpus_store)
            parser.parse(file_content)

            # Process the same data with HeaderBody Parser
            parser = phb.Parser(corpus_store)
            parser.parse(file_content)

        # Export the parsed data into file
        print ("Exporting the result...")
        return corpus_store.export_corpus(output_dir)

    print ("Total", len(files), "files to process.")
    output_path = process(files)
    print ("Exported:", output_path)

