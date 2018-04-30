# Setup Corpus Builder

## Setup Environment (Windows + Python 3)
HTML Parser is develped on Windows + Python 3 and currently (as of Dec.2017) it runs on Windows only. Mac/Unit is supposed to be eligible, but due to the difference of Python version and the default file encoding type (UTF, ECU etc, too complicated. Plus, the HTML files downloaded from APLaC site is all in Shift-JIS), it ended up in sticking to Windows environment.

### Things required in advance
* Python 3.5
* pip

## Required Python Libraries
```
pip install chardet
pip install beautifulsoup4
```

### Check Installation and Test
Run the unit tests and see if they run all OK.
```
python test_aplac.py
python test_parsers.py
python test_resources.py
python test_utils.py
```

To debug with Visual Studio Code, open the CorpusBuilder folder as the project directory, and run the each py file.

