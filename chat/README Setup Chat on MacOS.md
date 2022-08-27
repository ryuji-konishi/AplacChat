# Setup Chat on MacOS
This document describes how to setup an environment for the local development of APLaC Chat including training and inference.

## Setup Environment (MacOS 10.13 + Python 3.7)
MacOS 10.13 and Python 3.7 are used to setup Tensorflow. The matched version of Tensorflow is 2.6.5 which is later automatically decided during the installation process by the combination of MacOS version and Python version.
Follow the steps below to setup.

Before proceeding, check the current latest version of Tensorflow and its corresponding Python version in below.

https://cloud.google.com/ai-platform/training/docs/runtime-version-list

### Things required in advance
* Python 3.7
* pip for Python 3.7

### Things to be installed
* virtualenv
* Tensorflow
* Tensorflow Addons
* Google Cloud SDK

### Switching between Python 2 and Python 3
Just to leave a note, switching between Python versions was done by editing the PATH environment varilabe in the file below.
```
~/.bash_profile
```

### Installing Tensorflow
#### 1. Upgrade pip and check Tensorflow version
Before proceeding, you should upgrade pip to the latest version with command below.
```
python3.7 -m pip install --upgrade pip
```
And check the current latest version of Tensorflow, which is decided by pip command.
```
pip index versions tensorflow
```

As of Aug.2022, version 2.7.3 is returned by the above command, while 2.6.5 was actually installed in the following steps. It might be due to MacOS version limitation which was conditioned during the package installation process (not 100% sure). Thus, you might need to run the installation steps below to find out the actual version.

#### 2. Install virtualenv
```
pip install --upgrade virtualenv
```
#### 3. Create virtualenv environment
```
virtualenv --system-site-packages ~/prg/virtualenv/tf265p37
```
#### 4. Activate the environment
Create an alias that activates the virtual environment.
```
alias activate_tf265p37="source /Users/ryuji/prg/virtualenv/tf265p37/bin/activate"
```
Then re-open the terminal to refresh. Then type the command to activate the environment.
```
activate_tf265p37
```

It is better to add the above alias in ~/.bash_profile so that the alias becomes available always.
```
vim ~/.bash_profile
```

#### 5. Install tensorflow into virtualenv
```
pip install tensorflow
pip install tensorflow-addons
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
The installation is done by downloading the archive file and place its extract. Download the archive following the steps described in [here](https://cloud.google.com/sdk/docs/install-sdk).

For now it's placed under:
```
~/prg/tensorflow/google-cloud-sdk
```
#### Set PATH
The SDK doesn't install itself but setting its PATH is required.
Edit the virtualenv's activate file by appending the following line. By doing this, Google Cloud SDK becomes available when the virtual environment is activated.
The file edited:
```
~/prg/virtualenv/tf265p37/bin/activate
```
The line added:
```
export PATH=/Users/ryuji/prg/tensorflow/google-cloud-sdk/bin:$PATH
```
