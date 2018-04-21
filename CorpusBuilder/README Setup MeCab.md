# MeCab Installtion

This document describes the installation steps of MeCab morphological analyzer and its Python library into Windows and Linux systems with the following system configurations.

* Windows
 * Windows 10 64 bit
 * Python 3
* Linux
 * Amazon Linux 2
 * Python 2

## Installation Steps for Windows
[Reference](https://qiita.com/satetsu007/items/187e5a3f0ed0b898b152)

### 1. Install MeCab executable
Download the Windows version installer from [here](http://taku910.github.io/mecab/#download).
Choose UTF-8 as the dictionary character set.
The program is instaled in ```C:\Program Files (x86)\MeCab```

### 2. Download Python Binding Script
Download from the same site, the Python binding script mecab-python-0.996.tar.gz file. The direct link is [here](https://drive.google.com/drive/folders/0B4y35FiV1wh7fjQ5SkJETEJEYzlqcUY4WUlpZmR4dDlJMWI5ZUlXN2xZN2s2b0pqT3hMbTQ).

Extract the archive and edit setup.py as below.
```
#!/usr/bin/env python

from distutils.core import setup, Extension

setup(name = "mecab-python",
    version = '0.996',
    py_modules=["MeCab"],
    ext_modules = [
        Extension("_MeCab",
            ["MeCab_wrap.cxx",],
            include_dirs=[r'C:\Program Files (x86)\MeCab\sdk'],
            library_dirs=[r'C:\Program Files (x86)\MeCab\sdk'],
            libraries=['libmecab'])
            ])
```

### 3. Install Visual Studio 2015 Community
What we need is VC++ compiler. Choose VC++ custom component during the installation.

### 4. Check the build version of Python
Start Python and run below. If 14.0 is shown all good.
```
from distutils.msvc9compiler import *
get_build_version()
```

### 5. Set ProductDir in Registry
Opne Windows registry editor and set the following value.
```
Key: HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\VisualStudio\14.0\Setup\VC
Name: ProductDir
Value: C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC
```
In my case, it's already set as above.

### 6. Modify mecab.h
Edit the file ```C:\Program Files (x86)\MeCab\sdk\mecab.h``` in below around line 775.
```
/**
 * Lattice class
 */
class MECAB_DLL_CLASS_EXTERN Lattice {
public:
  virtual void set_result(const char *str) = 0; // Add this line

  /**
   * Clear all internal lattice data.
   */
  virtual void clear()              = 0;
```

### 7. Integrate modified libmecab.dll
Go to [this site](http://neu101.seesaa.net/article/272153413.html) and download ```mecab-python-0.993.win-build.zip```.
Extract the zip file and get the following files under 64 folder:
- libmecab.dll
- libmecab.lib

Copy those files into ```mecab-python-0.996``` folder that you created in step 2.

### 8. Install MeCab
Within the folder ```mecab-python-0.996```, open the terminal and run the following commands.
```
python setup.py build
python setup.py install
```
Now you are able to import MeCab module when you run Python within this folder.
```
import MeCab
```
If you go other folder path, import fails. In that case move to the next step.

### 9. Copy MeCab Module to Global Module Path
If you are using Anaconda3, copy the libmecab.dll/lib files to the following path.
```
%HOMEPATH%\Anaconda3\Lib\site-packages
```

### 10. Test
Open the Python and run the script below.
import MeCab
mecab = MeCab.Tagger("-Ochasen")
print(mecab.parse("すもももももももものうち"))





## Installation Steps for Windows Method 2 (did not work)
[Reference](https://qiita.com/buruzaemon/items/975027cea6371b2c5ec3)

### 1. Install MeCab executable
Download the Windows version installer from [here](http://taku910.github.io/mecab/#download).
Choose UTF-8 as the dictionary character set.
The program is instaled in ```C:\Program Files (x86)\MeCab```

### 2. Install natto-py
```
pip install natto-py
```

### 3. Rebuild MeCab for 64bit
This step is required if your Windows is 64 bit. Following the instractions described [here](https://github.com/buruzaemon/natto-py/wiki/64-Bit-Windows).

### 4. Add Path
Add the following to the path.
```
C:\Program Files (x86)\MeCab\bin
```

### 5. Test
Start python and type the commands.
```
>>> from natto import MeCab
>>> nm = MeCab()
Could not initialize MeCab Model
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\ryuji\Anaconda3\lib\site-packages\natto\mecab.py", line 168, in __init__
    raise MeCabError(self._ERROR_NULLPTR.format('Model'))
natto.api.MeCabError: Could not initialize MeCab Model
```

