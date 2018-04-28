# Setup Amazon Linux Server EC2 Instance

**This setup is not complete due to build error of Bazel. Bazel version 0.5.4 was not able to install with yum command and this forced to bild from source. But building from source was failed with error. Bazel version 0.5.4 is required to build Tensorflow 1.4. Newer version of Bazel is installable with yum command, so let's wish the newer Tensorflow can be built from source in the future.**

This section describes how to create and setup an EC2 Linux instance on Amazon Web Service (AWS) with the basic software components and libraries required for running APLaC-Chat web server.

## Create EC2 Instance
Login to [AWS console](https://aws.amazon.com) and create an EC2 instance.
### 1. Choose AMI
Choose the following AMI from the list.

**Amazon Linux 2 LTS Candidate AMI 2017.12.0 (HVM), SSD Volume Type - ami-38708c5a**

Note **Amazon Linux AMI 2017.09.1 (HVM), SSD Volume Type - ami-942dd1f6** is not suitable as it doesn't have ```systemd``` command. [Reference](https://serverfault.com/questions/889248/how-to-enable-systemd-on-amazon-linux-ami)

### 2. Security Group
Add a new inbound rule for HTTP type as below:

| Field  | Value |
| ------------- | ------------- |
| Type | HTTP |
| Protocol | TCP |
| Port | 80 |
| Source | Custom 0.0.0.0/0 |

### 3. Download key pair
```
chmod 400 keypairfile.pem
```

### 4. Connect to the EC2 instance with SSH
```
ssh -i /path/to/your/keyfile ec2-user@your_public_dnsname_here
```
## Setup Basic Features

### Things to pre-exist
* Python 2.7

### Things to be installed
* NGINX
* virtualenv
* Tensorflow 1.4.0
* Flask
* Gunicorn
* Google Cloud SDK
* .NET Core 2.0
* Bazel
* numpy
* wheel
* pip
* git

### 1. Install tools with root user
```
sudo easy_install pip
sudo easy_install -U setuptools
sudo pip install --upgrade setuptools
sudo pip install --upgrade virtualenv
sudo yum update
sudo amazon-linux-extras install nginx1.12
sudo yum install git
sudo pip install flask
sudo pip install gunicorn
```

### 2. Setup .NET Core 2.0
The installation steps are described in the [.NET Core 2.0 release note on github](
https://github.com/dotnet/core/blob/master/release-notes). Refer to the latest release version before proceeding.

Here we want to get the latest SDK. In the above site, there are also ‘runtime’ and ‘hosting’ installations, but what we want is SDK because we will build the frontend project on the machine.

```
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[packages-microsoft-com-prod]\nname=packages-microsoft-com-prod \nbaseurl=https://packages.microsoft.com/yumrepos/microsoft-rhel7.3-prod\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/dotnetdev.repo'
sudo yum install libunwind libicu
sudo yum install dotnet-sdk-2.1.4
```

### 3. Setup Tensorflow
Tensorflow is installed being built from source code for the purposes of better performance. We use CPU version of Tensorflow which can be built optimized for the  accelerator the CPU architecture provides.

https://www.tensorflow.org/install/install_sources

In the above page, the required version configurations for building Tensorflow is listed as below.

| Tensorflow | Python | Compiler | Bazel |
| ------------- | ------------- | ------------- | ------------- |
| 1.7.0 | 2.7, 3.3 - 3.6 | GCC 4.8 | 0.10.0 |
| 1.6.0 | 2.7, 3.3 - 3.6 | GCC 4.8 | 0.9.0 |
| 1.5.0 | 2.7, 3.3 - 3.6 | GCC 4.8 | 0.8.0 |
| 1.4.0 | 2.7, 3.3 - 3.6 | GCC 4.8 | 0.5.4 |

#### 1. Prepare environment for Linux

Install gcc tools.
```
# check which version is avalalble to install
yum list available | grep gcc
sudo yum install compat-gcc-48*
# sudo yum groupinstall "Development Tools"
```

Install TensorFlow Python dependencies.
```
sudo pip install numpy
# sudo pip install dev
sudo pip install wheel
```

#### Install Bazel
To get the lastest version, you can use yum as follows. But this is not usually useful because you need a specifi version.
```
cd ~
curl -O https://copr.fedorainfracloud.org/coprs/vbatts/bazel/repo/epel-7/vbatts-bazel-epel-7.repo
sudo mv ./vbatts-bazel-epel-7.repo /etc/yum.repos.d/
sudo yum install bazel
```

To install version 0.5.4, the above yum command doesn't work (yum install bazel 0.5.4 doesn't work). You need to build from source.
First create a directory for Bazel.
```
cd ~
mkdir bazel
cd bazel
```

Visit [Bazel release page](https://github.com/bazelbuild/bazel/releases) and download bazel-<version>-dist.zip.
```
wget -O bazel-0.5.4-dist.zip https://github.com/bazelbuild/bazel/releases/download/0.5.4/bazel-0.5.4-dist.zip
unzip bazel-0.5.4-dist.zip
rm bazel-0.5.4-dist.zip
```

You need Java to build Bazel.
```
sudo yum install java-1.8.0*
```

Before building bazel, increase the heap size for Java otherwise building will fail with out of memory error.
```
export _JAVA_OPTIONS="-Xmx1g"
# check the heap size
java -XshowSettings:vm
```

Start building Bazel.
```
./compile.sh
```

This is failed with error.
```
ERROR: /home/ec2-user/bazel/src/main/java/com/google/devtools/build/lib/BUILD:117:1: Building src/main/java/com/google/devtools/build/lib/libconcurrent.jar (18 source files) failed: Worker process sent response with exit code: 1.
java.lang.InternalError: Cannot find requested resource bundle for locale en_US
	at com.sun.tools.javac.util.JavacMessages.getBundles(JavacMessages.java:128)
	at com.sun.tools.javac.util.JavacMessages.getLocalizedString(JavacMessages.java:147)
	at com.sun.tools.javac.util.JavacMessages.getLocalizedString(JavacMessages.java:140)
	at com.sun.tools.javac.util.Log.localize(Log.java:788)
	at com.sun.tools.javac.util.Log.printLines(Log.java:586)
	at com.sun.tools.javac.api.JavacTaskImpl.handleExceptions(JavacTaskImpl.java:170)
	at com.sun.tools.javac.api.JavacTaskImpl.doCall(JavacTaskImpl.java:96)
	at com.sun.tools.javac.api.JavacTaskImpl.call(JavacTaskImpl.java:90)
	at com.google.devtools.build.buildjar.javac.BlazeJavacMain.compile(BlazeJavacMain.java:105)
	at com.google.devtools.build.buildjar.SimpleJavaLibraryBuilder$1.invokeJavac(SimpleJavaLibraryBuilder.java:106)
	at com.google.devtools.build.buildjar.ReducedClasspathJavaLibraryBuilder.compileSources(ReducedClasspathJavaLibraryBuilder.java:53)
	at com.google.devtools.build.buildjar.SimpleJavaLibraryBuilder.compileJavaLibrary(SimpleJavaLibraryBuilder.java:109)
	at com.google.devtools.build.buildjar.SimpleJavaLibraryBuilder.run(SimpleJavaLibraryBuilder.java:117)
	at com.google.devtools.build.buildjar.BazelJavaBuilder.processRequest(BazelJavaBuilder.java:100)
	at com.google.devtools.build.buildjar.BazelJavaBuilder.runPersistentWorker(BazelJavaBuilder.java:67)
	at com.google.devtools.build.buildjar.BazelJavaBuilder.main(BazelJavaBuilder.java:45)
Caused by: java.util.MissingResourceException: Can't find bundle for base name com.google.errorprone.errors, locale en_US
	at java.util.ResourceBundle.throwMissingResourceException(ResourceBundle.java:1573)
	at java.util.ResourceBundle.getBundleImpl(ResourceBundle.java:1396)
	at java.util.ResourceBundle.getBundle(ResourceBundle.java:854)
	at com.sun.tools.javac.util.JavacMessages.lambda$add$0(JavacMessages.java:106)
	at com.sun.tools.javac.util.JavacMessages.getBundles(JavacMessages.java:125)
	... 15 more
Target //src:bazel failed to build
```


#### 2. Clone the TensorFlow repository
The source code is to be placed under /home/ec2-user, version 1.4 is checked out.

```
git clone https://github.com/tensorflow/tensorflow
cd tensorflow
git checkout r1.4
```

#### 3. Configure the TensorFlow installation.
```
[ec2-user@ip-172-31-7-94 tensorflow]$ ./configure 
Extracting Bazel installation...
You have bazel 0.12.0- (@non-git) installed.
Please specify the location of python. [Default is /usr/bin/python]: 

Found possible Python library paths:
  /usr/lib/python2.7/site-packages
  /usr/lib64/python2.7/site-packages
Please input the desired Python library path to use.  Default is [/usr/lib/python2.7/site-packages]

Do you wish to build TensorFlow with jemalloc as malloc support? [Y/n]: 
jemalloc as malloc support will be enabled for TensorFlow.

Do you wish to build TensorFlow with Google Cloud Platform support? [Y/n]: n
No Google Cloud Platform support will be enabled for TensorFlow.

Do you wish to build TensorFlow with Hadoop File System support? [Y/n]: n
No Hadoop File System support will be enabled for TensorFlow.

Do you wish to build TensorFlow with Amazon S3 File System support? [Y/n]: n
No Amazon S3 File System support will be enabled for TensorFlow.

Do you wish to build TensorFlow with XLA JIT support? [y/N]: n
No XLA JIT support will be enabled for TensorFlow.

Do you wish to build TensorFlow with GDR support? [y/N]: n
No GDR support will be enabled for TensorFlow.

Do you wish to build TensorFlow with VERBS support? [y/N]: n
No VERBS support will be enabled for TensorFlow.

Do you wish to build TensorFlow with OpenCL support? [y/N]: n
No OpenCL support will be enabled for TensorFlow.

Do you wish to build TensorFlow with CUDA support? [y/N]: n
No CUDA support will be enabled for TensorFlow.

Do you wish to build TensorFlow with MPI support? [y/N]: n
No MPI support will be enabled for TensorFlow.

Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -march=native]: 


Add "--config=mkl" to your bazel command to build with MKL support.
Please note that MKL on MacOS or windows is still not supported.
If you would like to use a local MKL instead of downloading, please set the environment variable "TF_MKL_ROOT" every time before build.
Configuration finished
```

#### 4. Build the pip package

Change this file
```
vim /home/ec2-user/.cache/bazel/_bazel_ec2-user/0ff5a3f6434c30269b5495d73aade5d5/external/io_bazel_rules_closure/closure/repositories.bzl
```
in line 69 from
_check_bazel_version("Closure Rules", "0.4.5")
to
_check_bazel_version("Closure Rules", "0.12.0-")



```
bazel build --config=opt --config=mkl --incompatible_load_argument_is_label=false //tensorflow/tools/pip_package:build_pip_package
```
