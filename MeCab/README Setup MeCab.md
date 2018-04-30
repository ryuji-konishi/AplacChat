# MeCab
MeCab is a morphologinal analyzer that is used to tokenize Japanese sentenses. This MeCab Python module is used (called) by Corpus Builder to generate the vocaburary file when it applies the word-level tokenization.

**As of Apr.2018, this word-level tokenization is disabled due to the system performance resource limitation. Hence this MeCab module is not used. This document is left as a resource.**

# Installtion

This document describes the installation steps of MeCab morphological analyzer and its Python library into Windows, Mac and Linux systems with the following system configurations.

* Windows
  * Windows 10 64 bit
  * Python 3
* Mac OS
  * macOS High Sierra 10.13.3
  * Python 2
* Linux
  * Amazon Linux 2
  * Python 2

We also create a user dictionary for MeCab. The dictionary is generated on Windows system, and then it's exported on to Mac and Linux systems.

## Installation Steps for Amazon Linux
The target EC2 AMI is below.

**Amazon Linux 2 LTS Candidate AMI 2017.12.0 (HVM), SSD Volume Type - ami-38708c5a**

### Preparation
Before proceeding, install gcc tools and Python headers that are not included in the original Amazon EC2 AMI used here. They are required in the following steps.
```
sudo yum groupinstall "Development Tools"
sudo yum install python-devel
```

### 1. Install MeCab
Download the source file and compile it. If the following wget command failed to download, get the archive ```mecab-0.996.tar.gz``` from [here](http://taku910.github.io/mecab/#download).
```
cd ~
wget -O mecab-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE"
tar zxvf mecab-0.996.tar.gz
cd mecab-0.996
./configure
make
make check
sudo make install
```

### 2. Install IPA Dictionary
Download the dictionary file and compile it. If the following wget command failed to download, get the archive  ```mecab-ipadic-2.7.0-20070801.tar.gz``` from [here](http://taku910.github.io/mecab/#download).
```
cd ~
wget -O mecab-ipadic-2.7.0-20070801.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM"
tar zxvf mecab-ipadic-2.7.0-20070801.tar.gz
cd mecab-ipadic-2.7.0-20070801
./configure --with-charset=utf8
make
sudo make install
```

### 3. Add so file path
Modify ```/etc/ld.so.conf``` so that the MeCab's so file is loaded.
```
sudo vim /etc/ld.so.conf
```
Add the line below at the bottom of the file.
```
/usr/local/lib      # add this line at the bottom
```
Take effect of change by reloading.
```
sudo ldconfig
```

### 4. Install MeCab-Python
Download the script file and run it. If the following wget command failed to download, get the archive  ```mecab-python-0.996.tar.gz``` from [here](http://taku910.github.io/mecab/#download).
```
cd ~
wget -O mecab-python-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7UlJpaWJKM01KRVE"
tar zxvf mecab-python-0.996.tar.gz
cd mecab-python-0.996
```
Before running ```setup.py```, the file path to ```mecab-config``` needs to be a full path. Update ```setup.py``` by replacing 'mecab-config' by '/usr/local/bin/mecab-config'.
```
vim setup.py
```
Now run the setup.
```
python setup.py build
sudo python setup.py install
```

## Installation Steps for Mac
References
* http://ikekou.jp/blog/archives/2736
* https://qiita.com/nkjm/items/913584c00af199794257

### 1. Create the Installation Directory
```
sudo mkdir /usr/local/mecab
```

### 2. Install MeCab
Download the source file and compile it. If the following wget command failed to download, get the archive ```mecab-0.996.tar.gz``` from [here](http://taku910.github.io/mecab/#download).
```
cd ~/Downloads
wget -O mecab-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE"
tar zxfv mecab-0.996.tar.gz
cd mecab-0.996
./configure --enable-utf8-only --prefix=/usr/local/mecab
make
sudo make install
```

### 3. Install IPA Dictionary
Download the dictionary file and compile it. If the following wget command failed to download, get the archive  ```mecab-ipadic-2.7.0-20070801.tar.gz``` from [here](http://taku910.github.io/mecab/#download).
```
cd ~/Downloads
wget -O mecab-ipadic-2.7.0-20070801.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM"
tar zxfv mecab-ipadic-2.7.0-20070801.tar.gz
cd mecab-ipadic-2.7.0-20070801
./configure --prefix=/usr/local/mecab --with-mecab-config=/usr/local/mecab/bin/mecab-config --with-charset=utf8
make
sudo make install
```

### 4. Add Path
Add the path to MeCab
```
vim ~/.profile
```
```
export PATH=/usr/local/mecab/bin:$PATH
```
Reload .profile.
```
. ~/.profile
```

### 5. Install MeCab-Python
Download the script file and run it. If the following wget command failed to download, get the archive  ```mecab-python-0.996.tar.gz``` from [here](http://taku910.github.io/mecab/#download).
```
cd ~/Downloads
wget -O mecab-python-0.996.tar.gz "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7UlJpaWJKM01KRVE"
tar zxfv mecab-python-0.996.tar.gz
cd mecab-python-0.996
export CFLAGS=-Qunused-arguments
export CPPFLAGS=-Qunused-arguments
python setup.py build
python setup.py install
```

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
Copy the following files into ```mecab-python-0.996``` folder that you created in step 2.
- [libmecab.dll](./win/libmecab.dll)
- [libmecab.lib](./win/libmecab.lib)

Those files are required to run setup.py script on Windows systems because the original setup.py script is not Windows compatible. The above files are downloaded from [this site](http://neu101.seesaa.net/article/272153413.html) archived in ```mecab-python-0.993.win-build.zip```. You can find them under '64' folder.
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
```
import MeCab
mecab = MeCab.Tagger("-Ochasen")
print(mecab.parse("すもももももももものうち"))
```

## MeCab User Dictionary Configuration
We create the user dictionary file of MeCab in which there are additional custom words registered. First we create the user dictionary file (user.dic) on Windows, and then we import it to Linux system.

### 1. Create Dictionary File
The dictionary file (*.dic) is created from csv file with a utility command ```mecab-dict-index``` which is installed by MeCab. We use this command to create user.dic file as below.
```
SET USER_CSV_PATH=C:\Tmp\user.csv
SET IPA_DIC_PATH="C:\Program Files (x86)\MeCab\dic\ipadic"
SET USER_DIC_NAME=user.dic
SET CHAR_ENCODING=utf8

mecab-dict-index.exe -d %IPA_DIC_PATH% -u %USER_DIC_NAME% -f %CHAR_ENCODING% -t %CHAR_ENCODING% %USER_CSV_PATH%
```
- USER_CSV_PATH is the file path to the csv file which is the source of the dictionary data.
- IPA_DIC_PATH is the MeCab system dictionary that you've chosen during the installation. For Windows IPA dictionary is installed in default.
- USER_DIC_NAME is the dictionary file name to be created.
- CHAR_ENCODING is the character encoding of the csv file and dictionary file.

The above command is stored in a Windows bat file ```user_dic_compile.bat``` in the repository.

### 2. Register the Dictionary File
The generated user.dic file needs to be copied to the target system and registered to MeCab.

#### Windows
The user.dic file is assumed to exist under ```C:\prg\aplac\MeCab```.

Open ```C:\Program Files (x86)\MeCab\etc\mecabrc``` and add the following line. The file path has to be absolute.
```
userdic = C:\prg\aplac\MeCab\user.dic
```

#### Mac
The user.dic file is assumed to exist under ```~/prg/aplac/MeCab```.

Open ```/usr/local/mecab/etc/mecabrc```
```
sudo vim /usr/local/mecab/etc/mecabrc
```
and add the following line.
```
userdic = /Users/ryuji/prg/aplac/MeCab/user.dic
```


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


