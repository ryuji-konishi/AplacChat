# Setup Chat on MacOS

## Setup Environment (MacOS 10.13 + Python 3)
MacOS 10.13 and Python 3.7 are used to setup Tensorflow. The matched version of Tensorflow is 2.6.5 which is later automatically decided during the installation process by the combination of MacOS version and Python version.
This environment is for the local development of APLaC Chat including training and inference. Follow the steps below to setup.

Before proceeding, check the current latest version of Tensorflow and its corresponding Python version in below.

https://cloud.google.com/ai-platform/training/docs/runtime-version-list

### Things required in advance
* Python 3.7
* easy_install, pip

### Things to be installed
* virtualenv
* Tensorflow
* Google Cloud SDK

### Installing Tensorflow
#### 1. Upgrade pip and check Tensorflow version
Before proceeding, you should upgrade pip to the latest version with command below.
```
python3.7 -m pip install --upgrade pip
```
And check the current latest version of Tensorflow, which is decided by pip command.
```
pip show tensorflow
```
As of Aug.2022, version 2.6.5 is returned.

#### 2. Install virtualenv
```
pip install --upgrade virtualenv
```
#### 3. Create virtualenv environment
```
virtualenv --system-site-packages ~/prg/virtualenv/tf265p37
```
#### 4. Activate the environment
Create an alias that activates the virtual environment. Open ~/.bash_profile and add the following line.
```
alias activate_tf265p37="source /Users/ryuji/prg/virtualenv/tf265p37/bin/activate"
```
Then re-open the terminal to refresh. Then type the command to activate the environment.
```
activate_tf265p37
```
#### 5. Install tensorflow into virtualenv
```
pip install tensorflow
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
pip list --local
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
~/prg/virtualenv/tf140p2/bin/activate
```
The line added:
```
export PATH=/Users/ryuji/prg/tensorflow/google-cloud-sdk/bin:$PATH
```
