# Setup Chat/Frontend on Amazon Web Service EC2 Instance
This section describes how to set up both Chat and Frontend components on to the same EC2 Linux instance on Amazon Web Service (AWS). 

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
## Setup Environment

### 1. Install tools with root user
```
sudo easy_install pip
sudo pip install --upgrade virtualenv
sudo yum update
sudo amazon-linux-extras install nginx1.12
sudo yum install git
```

### 2. Create a new user
```
sudo /usr/sbin/useradd apps
```
This user will be later used to run the web apps. This user has to exist before starting web server.

### 3. Setup web server

#### 1. Change the user
```
sudo vim /etc/nginx/nginx.conf
```
Replace this line ```user nginx;``` with ```user   apps;```

And in the http block, add this line ```server_names_hash_bucket_size 128;```

#### 2. Define a server block for the site:
```
sudo vim /etc/nginx/conf.d/virtual.conf
```

Paste in the below:
```
server {
    listen 80;
    server_name your_public_dnsname_here;

    location / {
        proxy_pass http://localhost:5051;
    }
}
```

Check the configuration.
```
sudo nginx -t -c /etc/nginx/nginx.conf
```

#### 3. Start NGINX
```
sudo systemctl enable nginx
sudo systemctl start nginx
# Check the status
systemctl status nginx
```
Now you can see '502 Bad Gateway' when you access to your EC2 instance domain URL with web browser. This means the web server is running.

### 3. Setup Database
Currently we use MariaDB as the main database of the app. Follow the instructions in (this document)(README%20Setup%20MariaDB%20on%20AWS%20EC2.md) to set up MariaDB.

### 4. Change user
```
sudo su apps
```
The following steps are done with this user.

### 5. Create the application directory
Create a folder ```~/prg``` where you place all your programs. Note this is apps user's folder, not ec2-user.

Then create ```~/prg/aplac``` folder by cloning the git repository.
```
cd ~/prg
git clone https://github.com/ryuji-konishi/AplacChat.git aplac
```

### 6. Setup Python virtual environment
This virtual environment is used for running the Chat component because it is a Python program.
#### 1. Create virtualenv environment
```
virtualenv --system-site-packages ~/prg/virtualenv/tf140py2
```

#### 2. Activate the environment
Create an alias that activates the virtual environment. This is only useful when you run Python on terminal for testing and checking. Since we use Linux daemon to run the app, we don't actually need this.


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

### 7. Setup .NET Core 2.0
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

Now .NET Core 2.0 SDK is installed. Check if the frontend project is able to build successfully.
```
cd ~/prg/aplac/frontend/src
dotnet build
```

#### 4. Create Database
Run Entity Framework Core commands for the initial creation and the migrations of database.
Before proceeding, the database connection string has to be set as environment variable.
```
export MYSQL_CONNECTION_APPDB="server=localhost;database=aplacchat;userid=apps;password=yourpassword;"
```

Note the above user 'apps' is created during MariaDB installation described in the earlier section. This user is supposed to have access to database 'aplacchat' and local access is only granted.

Enter the following command to execute the migration that creates a new schema 'aplacchat' in DB if doesn't exist.
```
dotnet ef database update
```

#### 5. Build .NET Core deployment package
```
dotnet publish --configuration Release --output bin
```
The published outcome is generated under ```~/prg/aplac/frontend/src/bin``` directory. This is referenced in frontend.service file and will be later used when you start Linux daemon.

## Start APLaC Chat Service
We use SystemD to run the Chat component as a Linux daemon. Get back to the root user before proceeding.

### 1. Register SystemD service file

Copy the service file ```chat.service``` to system location.
```
sudo cp /home/apps/prg/aplac/chat/chat.service /lib/systemd/system
```

Reload SystemD and enable the service, so it will restart on reboots.
```
sudo systemctl daemon-reload
sudo systemctl enable chat
```

### 2. Start the service manually
This is only required when you want to run hands-on. The service is supposed to start automatically after reboot.
```
sudo systemctl start chat
# Check the status
systemctl status chat
# Check the output log
journalctl --unit chat --follow
```

Now aplac chat is started and it should be accessible.

### 3. Test Chat
Send a POST http request to the chat infer URL that returns the inferred text result.
```
curl -d 'aaa' -H "Content-Type: text/plain" -X POST http://localhost:8000/infer
```

## Start APLaC Frontend Service
Same as Chat service described above, we use SystemD to run the Chat component as a Linux daemon. Get back to the root user before proceeding.

### 1. Set environment variables
Before starting frontend, you need to set the environment variables that are stored in ```frontend.env``` file, and this file is reference in the service definition file.

Open the file ```/home/apps/prg/aplac/frontend/frontend.env``` and modify the following environment variables.

```
ASPNETCORE_URLS=http://localhost:5051
CHAT_EMBED_URL=http://your_public_dnsname_here/Embed/Index
CHAT_INFER_URL=http://your_public_dnsname_here/infer
MYSQL_CONNECTION_APPDB="server=localhost;database=aplacchat;userid=apps;password=yourpassword;"
```

And copy the file to /etc/sysconfig directory.
```
sudo cp /home/apps/prg/aplac/frontend/frontend.env /etc/sysconfig
```

### 2. Register SystemD service file

Copy the service file to system location.
```
sudo cp /home/apps/prg/aplac/frontend/frontend.service /lib/systemd/system
```

Reload SystemD and enable the service, so it will restart on reboots.
```
sudo systemctl daemon-reload
sudo systemctl enable frontend
```

### 2. Start the service manually
This is only required when you want to run hands-on. The service is supposed to start automatically after reboot.
```
sudo systemctl start frontend
# Check the status
systemctl status frontend
# Check the output log
journalctl --unit frontend --follow
```

Now you can see the front end top page when you access to your EC2 instance domain URL with web browser.


Done!

## Reference
* https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/
* http://pmcgrath.net/running-a-simple-dotnet-core-linux-daemon
