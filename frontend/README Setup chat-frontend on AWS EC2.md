# Setup Chat/Frontend on Amazon Web Service EC2 Instance
This section describes how to set up both Chat and Frontend components on to the same EC2 Linux instance on Amazon Web Service (AWS). 

## Create EC2 Instance
Login to [AWS console](https://aws.amazon.com) and create an EC2 instance.
### 1. Choose AMI
Choose the following AMI from the list.

**Amazon Linux AMI 2017.09.1 (HVM), SSD Volume Type, 64 bit**

| Field  | Value |
| ------------- | ------------- |
| Type  |  t2.nano  |
| vCPUs  | 1  |
| Memory | 1GB |
| Storage | EBS only |

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
## Setup Environment

### 1. Install tools with root user
```
sudo easy_install pip
pip install --upgrade virtualenv
sudo yum install nginx
sudo yum install git
sudo yum install tmux
```
```tmux``` is used to run the web server in a separate session so that the web-server execution commands (gunicorn/dotnet) keep alive after exiting from ssh terminal.

### 2. Setup web server

#### 1. Forward HTTP requests from port 80 to our Flask app
```
sudo vim /etc/nginx/nginx.conf
```
Replace this line ```user nginx;``` with ```user   apps;```

And in the http block, add this line ```server_names_hash_bucket_size 128;```

#### 2. Define a server block for our site:
```
sudo vim /etc/nginx/conf.d/virtual.conf
```

Paste in the below:
```
server {
    listen 80;
    server_name your_public_dnsname_here;

    location /infer {
        proxy_pass http://localhost:8000/infer;
    }
    location / {
        proxy_pass http://localhost:5051;
    }
}
```

 Since two different web internal servers will run, the proxy setting of nginx becomes a bit complicated. The 'infer' path is specifically assigned to the Chat component, and all the other paths go to the frontend.

#### 3. Start the web server
```
sudo /etc/rc.d/init.d/nginx start
```
Now you can see '502 Bad Gateway' when you access to your EC2 instance domain URL with web browser. This is shown by nginx, and it is because currently no web page running for http://localhost:5051.

### 3. Create a new user
```
sudo /usr/sbin/useradd apps
sudo su apps
```
This user is used to run web-server apps. The following steps are done with this user.

### 4. Create the application directory
Create a folder ```~/prg``` where you place all your programs. Note this is apps user's folder, not ec2-user.

Then create ```~/prg/aplac``` folder by cloning the git repository.
```
cd ~/prg
git clone https://github.com/ryuji-konishi/AplacChat.git aplac
```

### 5. Setup Python virtual environment
This virtual environment is used for running the Chat component because it is a Python program.
#### 1. Create virtualenv environment
```
virtualenv --system-site-packages ~/prg/virtualenv/tf140py2
```

#### 2. Activate the environment
Create an alias that activates the virtual environment.
Open ~/.bashrc and add the following line.
```
alias activate_tf140py2="source /home/apps/prg/virtualenv/tf140py2/bin/activate"
```
Now activate the virtual environment before proceeding. The following installations are done in this env.
```
activate_tf140py2
```

#### 3. Install Tensorflow
```
pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.4.0-cp27-none-linux_x86_64.whl
```
If you got 'MemoryError', it is because the moemory is not enough to handle the file. Try not to use caching.
```
pip install --upgrade --no-cache-dir https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.4.0-cp27-none-linux_x86_64.whl
```

#### 4. Install Flask and Gunicorn
```
pip install flask
pip install gunicorn
```

### 6. Setup .NET Core 2.0
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

In the release note web page, get the URL for Linux runtime binaries and download it. As of Mar.2018 the following file is the latest version of SDK.
```
curl -o dotnet-sdk-2.1.4-linux-x64.tar.gz https://download.microsoft.com/download/1/1/5/115B762D-2B41-4AF3-9A63-92D9680B9409/dotnet-sdk-2.1.4-linux-x64.tar.gz
```

#### 3. Extract archive
Extract the archive and set path to ‘dotnet’ command inside.
```
tar zxf ./dotnet-sdk-2.1.4-linux-x64.tar.gz
export PATH=$PATH:$HOME/prg/dotnet/sdk
```


Now .NET Core 2.0 SDK is installed. Check if the frontend project is able to build successfully.
```
cd ~/prg/aplac/frontend/src
dotnet build
```

## Start APLaC Chat
We use tmux here so that the web server keeps running after closing the ssh terminal.

### 1. Start a new session on tumx
```
tmux new -s chat
```

### 2. Start aplac chat with gunicorn
```
activate_tf140py2
cd ~/prg/aplac/chat/
gunicorn run_infer_web:app -b localhost:8000
```
Now aplac chat is started and it should be accessible.

### 3. Test Chat
Send a POST http request to the following URL that returns the inferred text result.

http://your_public_dnsname_here/infer

### The configurations for Postman

_Authorization_

| Field  | Value |
| ------------- | ------------- |
| Type | No Auth |

_Headers_

| Field  | Value |
| ------------- | ------------- |
| Key | Content-Type |
| Value | text/plain |
| Description | (empty) |

_Body_

Choose 'raw' and 'Text' as data type, and then type in the inference data text into the text box.

### 4. Detach tmux
Type Ctrl+b and then d.

## Start APLaC Frontend
We use tmux here so that the web server keeps running after closing the ssh terminal.

### 1. Start a new session on tumx
```
tmux new -s frontend
```

### 2. Set environment variables
```
export ASPNETCORE_URLS=http://localhost:5051
export CHAT_EMBED_URL=http://your_public_dnsname_here/Embed/Index
export CHAT_INFER_URL=http://your_public_dnsname_here/infer
```

### 3. Start aplac frontend with dotnet
```
cd ~/prg/aplac/frontend/src
dotnet build
dotnet run
```

Now you can see the front end top page when you access to your EC2 instance domain URL with web browser.

### 3. Detach tmux
Type Ctrl+b and then d.


Now you can exit from ssh terminal.

## Manage Apps
The following commands are useful when you manage the web server process and tmux session.

### tmux
- List sessions: ```tmux list-sessions```
- Reattach to session: ```tmux attach -t chat```

### gunicorn
- Check if gunicorn running: ```ps ax|grep gunicorn```
- Stop gunicorn: ```sudo pkill gunicorn```

## Trouble Shooting
### When the EC2 instance Public DNS is changed:
Replace the DNS in the following file:
```
$ sudo vi /etc/nginx/conf.d/virtual.conf
```
(if nginx is already started) Restart nginx
```
$ sudo /etc/rc.d/init.d/nginx restart
```

Note you also need to change the URL in the front-end web page.

## Reference
https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/
