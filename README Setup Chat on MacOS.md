# Setup Chat on MacOS

## Setup Environment (MacOS + Python 2)
Python 2 is used because Google Cloud Machine Learning Engine doesn't support Python3 as of Dec.2017. Also Tensorflow version 1.2.0 is required because Google Cloud Platform doesn't support 1.4 as of Dec.2017.
This environment is for both development and actual use of APLaC Chat training and inference. Follow the steps below to setup.

### Things required in advance
* Tensorflow only supports Mac OS 10.11.
* easy_install (this is the Apple's pre-installed version of Python)

### Things to be installed
* pip
* virtualenv
* Tensorflow 1.2.0
* Google Cloud SDK

### Installing Tensorflow
#### 1. Install pip
```
$ sudo easy_install pip
```
If easy_install doesn't work with error like "Could not find suitable distribution for Requirement.parse('pip')", go to https://www.python.org/downloads/mac-osx/ and download the recent build of Python2, run the installer.

#### 2. Install virtualenv
```
$ pip install --upgrade virtualenv
```
#### 3. Create virtualenv environment
```
$ virtualenv --system-site-packages ~/prg/virtualenv/tf120p2
```
#### 4. Activate the environment
Create an alias that activates the virtual environment. Open ~/.bash_profile and add the following line.
```
alias activate_tf120p2="source /Users/ryuji/prg/virtualenv/tf120p2/bin/activate"
```
Then re-open the terminal to refresh. Then type the command to activate the environment.
```
$ activate_tf120p2
```
#### 5. Install tensorflow (CPU version) into virtualenv
Download the wheel file from https://pypi.python.org/pypi/tensorflow/1.2.0, save the file locally, and run the pip command below.
```
$ pip install --upgrade ~/prg/tensorflow/tensorflow-1.2.0-cp27-cp27m-macosx_10_11_x86_64.whl
```
#### Check
Check if Tensorflow is successfully installed.
```
(tensorflow)C:> Python
>>> import tensorflow as tf
>>> print (tf.__version__)
```
Check what packages are installed.
```
$ pip list --local
```

### Installing Google Cloud SDK
Google Cloud SDK is required to access to Google Cloud Platform (GCP). In our project, GCP is used to train and infer in both locally and remotelly (on cloud).
#### Download SDK
The installation is done by downloading the archive file and place its extract. For now it's placed under:
```
~/prg/tensorflow/google-cloud-sdk
```
#### Set PATH
The SDK doesn't install itself but setting its PATH is required.
Edit the virtualenv's activate file by appending the following line. By doing this, Google Cloud SDK becomes available when the virtual environment is activated.
The file edited:
```
~/prg/virtualenv/tf120p2/bin/activate
```
The line added:
```
export PATH=/Users/ryuji/prg/tensorflow/google-cloud-sdk/bin:$PATH
```
