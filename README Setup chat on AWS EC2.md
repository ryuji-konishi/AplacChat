# Setup Chat on Amazon Web Service EC2 Instance

## Create EC2 Instance
Login to AWS console and create an EC2 instance.
### 1. Choose AMI
Choose the following AMI from the list.

**Amazon Linux AMI 2017.09.1 (HVM), SSD Volume Type**

| Field  | Value |
| ------------- | ------------- |
| Type  |  t2.micro  |
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

## Setup Environment

### 1. Connect to the EC2 instance with SSH
'ssh' command format
```
ssh -i /path/to/your/keyfile ec2-user@your_public_dnsname_here
```
Example
```
ssh -i AWS/MacBookAir13.pem ec2-user@ec2-54-252-240-215.ap-southeast-2.compute.amazonaws.com
```

### 2. Install tools with root user
```
$ sudo easy_install pip
$ pip install --upgrade virtualenv
$ sudo yum install nginx
$ sudo yum install git
```

### 3. Create a new user
```
$ sudo /usr/sbin/useradd apps
$ sudo su apps
```

### 4. Install tools into the user's virtual environment

#### 1. Create virtualenv environment
```
$ virtualenv --system-site-packages ~/prg/virtualenv/tf120py2
```

#### 2. Activate the environment
Create an alias that activates the virtual environment.
Open ~/.bashrc and add the following line.
```
alias activate_tf120py2="source /home/apps/prg/virtualenv/tf120py2/bin/activate"
```
Re-open the terminal.
```
$ activate_tf120py2
```

#### 3. Install Tensorflow
```
$ pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.2.0-cp27-none-linux_x86_64.whl
```

#### 4. Install Flask and Gunicorn
```
$ pip install flask
$ pip install gunicorn
```

#### 5. Get back to the root user
```
$ exit
```

### 5. Setup web server

#### 1. Forward HTTP requests from port 80 to our Flask app
```
sudo vi /etc/nginx/nginx.conf
```
Replace this line ```user nginx;``` with ```user   apps;```

And in the http block, add this line ```server_names_hash_bucket_size 128;```

#### 2. Define a server block for our site:
```
$ sudo vi /etc/nginx/conf.d/virtual.conf
```

Paste in the below:
```
server {
  listen 80;
  server_name your_public_dnsname_here;

  location / {
  proxy_pass http://127.0.0.1:8000;
  }
}
```

#### 3. Start the web server
```
$ sudo /etc/rc.d/init.d/nginx start
```

## Start APLaC Chat
### 1. Login with SSH and the apps user.
```
$ sudo su apps
```

### 2. Create the application directory
```
$ cd ~/prg
$ mkdir aplac
```

or clone from github
```
$ git clone https://github.com/ryuji-konishi/AplacChat.git aplac
```

### 3. Upload the aplac code
```
scp -i AWS/MacBookAir13.pem aplac.zip ec2-user@ec2-54-252-240-215.ap-southeast-2.compute.amazonaws.com:~/.
```

### 4. Start aplac chat
```
$ activate_tf120py2
$ cd ~/prg/aplac/chat/
$ gunicorn run_infer_web:app -b localhost:8000
```

## How to run
Send a POST http request to the following URL that returns the inferred text result.

http://ec2-54-252-240-215.ap-southeast-2.compute.amazonaws.com/train

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

## Reference
https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/
