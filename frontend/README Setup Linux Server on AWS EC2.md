# Setup Amazon Linux Server EC2 Instance
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

### Things to be installed
* NGINX
* virtualenv
* Tensorflow 1.4.0
* Flask
* Gunicorn
* Google Cloud SDK
* .NET Core 2.0

### 1. Install tools with root user
```
sudo easy_install pip
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

#### 1. Installation method
Here we want to get the latest SDK. In the above site, there are also ‘runtime’ and ‘hosting’ installations, but what we want is SDK because we will build the frontend project on the machine.

To install SDK, according to the document, a command ```sudo yum install dotnet-sdk-2.x.x``` is supposed to work.

But, as of Mar.2018, this command didn’t work with an error saying ‘openssl-libs’ missing.
So we will follow the binary archive installation method.

#### 2. Download SDK
Note the following work will be done within ```~/prg``` directory of ```apps``` user.

Creat a directory ```~/prg/dotnet/sdk```
```
cd ~/prg
mkdir dotnet && cd dotnet && mkdir sdk && cd sdk
```

In the release note web page, get the URL for Linux SDK binaries and download it. As of Mar.2018 the following file is the latest version of SDK.
```
curl -o dotnet-sdk-2.1.4-linux-x64.tar.gz https://download.microsoft.com/download/1/1/5/115B762D-2B41-4AF3-9A63-92D9680B9409/dotnet-sdk-2.1.4-linux-x64.tar.gz
```

#### 3. Extract archive
Extract the archive and set path to ‘dotnet’ command inside.
```
tar zxf ./dotnet-sdk-2.1.4-linux-x64.tar.gz
```

Open ~/.bashrc and add the following line.
```
export PATH=$PATH:$HOME/prg/dotnet/sdk
```

### 3. Install Tensorflow
Tensorflow is installed being built from source code for the purposes of better performance. We use CPU version of Tensorflow which can be built optimized for the  accelerator the CPU architecture provides.

https://www.tensorflow.org/install/install_sources




