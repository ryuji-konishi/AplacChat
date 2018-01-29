

Create EC2 Instance
Login to AWS console and create an EC2 instance.
Choose AMI
Choose the following AMI from the list.
[Amazon Linux AMI 2017.09.1 (HVM), SSD Volume Type]
Type: t2.micro, vCPUs: 1, Memory: 1GB, Storage: EBS only

Security Group
Add a new inbound rule for HTTP type as below:
Type = HTTP, Protocol = TCP, Port = 80, Source = Custom 0.0.0.0/0

Download key pair
chmod 400 keypairfile.pem

Setup Environment
Connect to the EC2 instance with SSH
'ssh' command format
ssh -i /path/to/your/keyfile ec2-user@your_public_dnsname_here
Example
ssh -i AWS/MacBookAir13.pem ec2-user@ec2-54-252-240-215.ap-southeast-2.compute.amazonaws.com

Install tools with root user
$ sudo easy_install pip
$ pip install --upgrade virtualenv
$ sudo yum install nginx
$ sudo yum install git

Create a new user
$ sudo /usr/sbin/useradd apps
$ sudo su apps

 Install tools into the user's virtual environment

Create virtualenv environment
$ virtualenv --system-site-packages ~/prg/virtualenv/tf120py2

Activate the environment
Create an alias that activates the virtual environment.
Open ~/.bashrc and add the following line.
alias activate_tf120py2="source /home/apps/prg/virtualenv/tf120py2/bin/activate"
Re-open the terminal.

$ activate_tf120py2

Install Tensorflow
$ pip install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.2.0-cp27-none-linux_x86_64.whl

Install Flask and Gunicorn
$ pip install flask
$ pip install gunicorn

Get back to the root user
$ exit

Setup web server
Forward HTTP requests from port 80 to our Flask app
sudo vi /etc/nginx/nginx.conf

Replace this line:
user   nginx;
with this:
user   apps;
and in the http block, add this line:
server_names_hash_bucket_size 128;

Define a server block for our site:
$ sudo vi /etc/nginx/conf.d/virtual.conf

Paste in the below:
server {
  listen 80;
  server_name your_public_dnsname_here;

  location / {
  proxy_pass http://127.0.0.1:8000;
  }
}

Start the web server
$ sudo /etc/rc.d/init.d/nginx start

Start APLaC Chat
Login with SSH and the apps user.
$ sudo su apps

Create the application directory
$ cd ~/prg
$ mkdir aplac

or clone from github
$ git clone https://github.com/ryuji-konishi/AplacChat.git aplac

Upload the aplac code
scp -i AWS/MacBookAir13.pem aplac.zip ec2-user@ec2-54-252-240-215.ap-southeast-2.compute.amazonaws.com:~/.

Start aplac chat
$ activate_tf120py2
$ cd ~/prg/aplac/chat/
$ gunicorn run_infer_web:app -b localhost:8000

How to run
Send a POST http request to the following URL that returns the inferred text result.
http://ec2-54-252-240-215.ap-southeast-2.compute.amazonaws.com/train

The configurations for Postman
[Authorization]
Type: No Auth
[Headers]
Key: "Content-Type"     Value: "text/plain"     Description: (empty)
[Body]
raw, Text

Trouble Shooting
When the EC2 instance Public DNS is changed:
Replace the DNS in the following file:
$ sudo vi /etc/nginx/conf.d/virtual.conf
(if nginx is already started) Restart nginx
$ sudo /etc/rc.d/init.d/nginx restart

Reference
https://www.matthealy.com.au/blog/post/deploying-flask-to-amazon-web-services-ec2/