# -*- coding: utf-8 -*-
import sys
sys.setrecursionlimit(2000) # This is to allow more recursive function calls for bigger sized HTML files. The default is 1000 for Windows.

import os
import datetime
import codecs
import urllib.request
import shutil

import utils.file_utils as file_utils
import utils.corpus_utils as corpus_utils
import parsers.ParserAtomic as pat
import parsers.ParserAtomicHeaderBody as pah
import parsers.ParserHeaderBody as phb

def log(*arg):
    msg = u' '.join(arg)
    print (msg)
    f = codecs.open('cleaner.log', 'a', 'utf-8')        # appending
    t = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
    f.write(t + msg + '\n')
    f.close()

def check_contain(file_content, check_text):
    """ Retrun True if file_content string list contains check_text """
    for line in file_content:
        if check_text in line:
            return True
    return False

def download_html(html_path):
    html_path = html_path.replace(os.path.sep, '/')
    url = 'https://aplac.net/' + html_path
    local_filename, headers = urllib.request.urlretrieve(url)
    return local_filename       # the file is in the sytem temp folder

def clean(input_path):
    """ Clean the HTML files.
        - Check if HTML files are correctly readable. If not download the original file from the site again.
        - Check if HTML files contain 404 Not Found. Delete these files.
        input_path is either a folder path or file path, both in absolute path.
    """
    
    if os.path.isfile(input_path):
        print ("The input file is", input_path)
        files = [[input_path, os.path.basename(input_path)]]
    else:
        input_dir = input_path
        print ("The input directory is", input_dir)
        print ("Searching HTML files in the input directory...")
        files = file_utils.get_filelist_in_path("html", input_dir, True)

    # Parse the files and store the result into data store
    print ("Total", len(files), "files to process. Loading...")
    for idx, file in enumerate(files):
        f_abst = file[0]    # absolute path
        f_rel = file[1]     # relative path
        print ("(", idx, "of", len(files), ") file", f_rel)
        file_content = file_utils.read_filelist_any_encoding(f_abst)
        if (len(file_content) == 0):
            print(u"File read failed. Attempting to download the original file...")
            downloaded_file = download_html(f_rel)
            file_content = file_utils.read_filelist_any_encoding(downloaded_file)
            if (len(file_content) == 0):
                log(u"Failed to read file even with re-downloaded file", f_abst)
                continue
            else:
                print(u"Replaced with downloaded file", f_rel)
                shutil.copyfile(downloaded_file, f_abst)

        # Delete file if it contains 404 File Not Found
        if check_contain(file_content, "<title>404 File Not Found</title>"):
            log(u"Removed file containing \"404 File Not Found\"", f_abst)
            os.remove(f_abst)

    print ("Finished.")

def parse(input_path, output_dir):
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
        corpus_store = corpus_utils.CorpusStore()

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
            parser = phb.Parser(corpus_store, ['h1', 'h2', 'h3', 'h4', 'h5'])
            parser.parse(file_content)

        # Export the parsed data into file
        print ("Exporting the result...")
        return corpus_store.export_corpus(output_dir)

    print ("Total", len(files), "files to process.")
    output_path = process(files)
    print ("Exported:", output_path)


