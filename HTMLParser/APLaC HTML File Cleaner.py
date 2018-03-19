# -*- coding: utf-8 -*-
import os
import datetime
import utils.file_utils as file_utils
import codecs
import urllib.request
import shutil

# APLaC HTML File Cleaner
# - Check if HTML files are correctly readable. If not download the original file from the site again.
# - Check if HTML files contain 404 Not Found. Delete these files.

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


html_folder = "C:\\Tmp\\aplac\\html\\aplac.net"
# html_folder = "C:\\Tmp\\aplac\\decode error"

current_dir = os.path.dirname(os.path.realpath(__file__))

print ("Searching HTML files in the input directory...")
files = file_utils.get_filelist_in_path("html", html_folder, True)
# files = ["C:\\Tmp\\aplac\\html\\aplac.net\\gogaku\\crisis05.html"]
# Parse the files and store the result into data store
fileCount = len(files)
print (fileCount, "files to process.")

for idx, file in enumerate(files):
    f_abst = file[0]    # absolute path
    f_rel = file[1]     # relative path
    print ("(", idx, "of", fileCount, ") file", f_rel)
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
