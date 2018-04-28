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

### Things to pre-exist
* Python 2.7
* SQLite3

### Things to be installed
* NGINX
* virtualenv
* Google Cloud SDK
* .NET Core 2.0
* numpy
* pip
* git

### 1. Install tools with root user
```
sudo easy_install pip
sudo pip install --upgrade virtualenv
sudo yum update
sudo amazon-linux-extras install nginx1.12
sudo yum install git
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

### 3. Install Google Cloud SDK

#### Download SDK
The installation is done by downloading the archive file and place its extract. For now it's placed under:
```
wget -O google-cloud-sdk-199.0.0-linux-x86_64.tar.gz https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-199.0.0-linux-x86_64.tar.gz
tar zxvf google-cloud-sdk-199.0.0-linux-x86_64.tar.gz
```

Copy the folder under /opt.
```
sudo cp -R ./google-cloud-sdk /opt/
```

Delete the unused directory and file.
```
rm -r ~/google-cloud-sdk
rm google-cloud-sdk-199.0.0-linux-x86_64.tar.gz
```

#### Set PATH
We set google cloud SDK available for all users.
Create a file ```/etc/profile.d/google-cloud-sdk.sh``` with the content below.
```
sudo vim /etc/profile.d/google-cloud-sdk.sh
```
Add the line below.
```
export PATH=$PATH:/opt/google-cloud-sdk/bin
```

#### Initialization
