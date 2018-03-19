import os
import sys
from chardet.universaldetector import UniversalDetector

def get_filelist_in_path(extension, path, sub_directory=True):
    """Return the list of files under the specified path. The list contains both the absolute path and relative path to the files."""
    ext = ".%s" % extension.lower()
    result = []
    if sub_directory:
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.lower().endswith(ext):
                    abst = os.path.join(root, f)
                    path_diff = root.replace(path, "")
                    if path_diff.startswith('\\'):      # remove the leading '\' to make it a relative path
                        path_diff = path_diff[1:]
                    rel = os.path.join(path_diff, f)
                    result.append((abst, rel))
    else:
        for f in os.listdir(path):
            abst = os.path.join(path, f)
            if os.path.isfile(abst) and f.lower().endswith(ext):
                result.append((abst, f))
    return result

def read_file_any_encoding(path):
    enc = detect_encoding(path)
    result = []
    try:
        f = open(path, "r", encoding=enc)
        result = f.read()
    except:
        pass
    finally:
        f.close()
    return result

def read_filelist_any_encoding(path):
    """ Return a list of text lines."""
    enc = detect_encoding(path)
    result = []
    try:
        f = open(path, "r", encoding=enc)
        result = f.read().splitlines()      # Use splitlines() so that the result list won't contain line-break.
        # result = f.readlines()
    except:
        print(sys.exc_info()[0])
    finally:
        f.close()
    return result

def detect_encoding(path):
    detector = UniversalDetector()
    f = open(path, "rb")
    for line in f:
        detector.feed(line)
        if detector.done: break
    detector.close()
    f.close()
    return detector.result['encoding']


if __name__ == "__main__":
    for f in get_filelist_in_path("html", "C:\\Ryuji\\Dropbox\\prg\\HTMLParser", False):
        print (read_file_in_utf8(f))
    print (get_filelist_in_path("html", "C:\\Ryuji\\Dropbox\\prg\\HTMLParser"))

