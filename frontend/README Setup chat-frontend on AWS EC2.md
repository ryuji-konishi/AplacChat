# Setup Chat/Frontend on Amazon Web Service EC2 Instance
This section describes how to set up both Chat and Frontend components on to the same EC2 Linux instance on Amazon Web Service (AWS). 

## Create EC2 Instance
Follow the steps described in [README Setup Linux Server on AWS EC2](README%20Setup%20Linux%20Server%20on%20AWS%20EC2.md) and create a Linux instance that has the following features installed.

* Python 2.7
* SQLite3
* NGINX
* virtualenv
* Flask
* Gunicorn
* Google Cloud SDK
* .NET Core 2.0
* numpy
* pip
* git

## Setup Chat/Frontend
To the Linux instance created above, follow the steps below to setup APLaC Chat/Frontend components.

In this section the followings are additionally installed.
* Flask
* Gunicorn
* TensorFlow 1.4

### 1. Create a new user
```
sudo /usr/sbin/useradd aplac
```
This user will be later used to run the web server. This user has to exist before starting web server.

### 2. Setup web server

#### 1. Change the user
```
sudo vim /etc/nginx/nginx.conf
```
Replace this line ```user nginx;``` with ```user   aplac;```

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
Currently SQLite3 is used as the main database of the app. SQLite comes as default in the Amazon EC2 AMI used.

### 4. Change user
```
sudo su aplac
cd ~
```
The following steps are done with this user.

Before proceeding, if not done yet, login to Google Cloud Platform with SDK command below. This command setups your Google user account configuration within the newly created user.
```
gcloud init
```

### 5. Create the application directory
Then create ```~/aplac``` folder by cloning the git repository.
```
git clone https://github.com/ryuji-konishi/AplacChat.git aplac
```

### 6. Setup Python virtual environment
This virtual environment is used for running the Chat component because it is a Python program.
#### 1. Create virtualenv environment
```
virtualenv --system-site-packages ~/virtualenv/tf140py2
```

#### 2. Activate the environment
Create an alias that activates the virtual environment. This is only useful when you run Python on terminal for testing and checking. Since we use Linux daemon to run the app, we don't actually need this.


Open ~/.bashrc and add the following line.
```
alias activate_tf140py2="source /home/aplac/virtualenv/tf140py2/bin/activate"
```
Now activate the virtual environment before proceeding. The following installations are done in this env.
```
activate_tf140py2
```

#### 3. Install Python Modules
The following Python modules are installed into the virtual environment.
```
pip install flask
pip install gunicorn
```

### 7. Install Tensorflow
Install TensorFlow into the above created virtual environment.
```
pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.4.0-cp27-none-linux_x86_64.whl
```
If you got 'MemoryError', it is because the moemory is not enough to handle the file. Try not to use caching.
```
pip install --upgrade --no-cache-dir https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.4.0-cp27-none-linux_x86_64.whl
```

### 8. Build Frontend

The frontend is a .NET Core 2.0 project. Build the project with .NET Core SDK.
```
cd ~/aplac/frontend/src
dotnet build
```

Before proceeding, the database connection string has to be set as environment variable. Note this value has to be also defined in ```~/aplac/frontend/frontend.env```.
```
export CONNECTION_APPDB="Data Source=file:/home/aplac/aplacchat.db"
```

Run Entity Framework Core commands for the initial creation and the migrations of database.
Enter the following command to execute the migration that creates a new schema 'aplacchat' in DB if doesn't exist.
```
dotnet ef database update
```

The final step is to publish the frontend project.
```
dotnet publish --configuration Release --output bin
```
The published outcome is generated under ```~/aplac/frontend/src/bin``` directory. This is referenced in frontend.service file and will be later used when you start Linux daemon.

## Start APLaC Chat Service
We use SystemD to run the Chat component as a Linux daemon. Get back to the root user before proceeding.

Before proceeding, make sure you have NMT data which is generated during NMT training. It is assumed that the NMT data is placed under ```~/data```.

### 1. Register SystemD service file

Copy the service file ```chat.service``` to system location.
```
sudo cp /home/aplac/aplac/chat/chat.service /lib/systemd/system
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

Open the file ```/home/aplac/aplac/frontend/frontend.env``` and modify the following environment variables.

```
ASPNETCORE_URLS=http://localhost:5051
CHAT_EMBED_URL=http://your_public_dnsname_here/Embed/Index
CHAT_INFER_URL=http://your_public_dnsname_here/infer
CONNECTION_APPDB="Data Source=file:/home/aplac/aplac/aplacchat.db"
```

And copy the file to /etc/sysconfig directory.
```
sudo cp /home/aplac/aplac/frontend/frontend.env /etc/sysconfig
```

### 2. Register SystemD service file

Copy the service file to system location.
```
sudo cp /home/aplac/aplac/frontend/frontend.service /lib/systemd/system
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
