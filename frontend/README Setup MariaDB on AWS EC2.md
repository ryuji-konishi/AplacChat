# Setup MariaDB on Amazon Web Service EC2 Instance
This section describes how to set up MariaDB on to the same EC2 Linux instance on Amazon Web Service (AWS) that is to host the Chat and Front-End components of APLaC-Chat.

## EC2 Instance
This document assumes that you:
 * have login to [AWS console](https://aws.amazon.com) and created an EC2 instance.
 * choose the AMI type below.
**Amazon Linux 2 LTS Candidate AMI 2017.12.0 (HVM), SSD Volume Type - ami-38708c5a**

## Setup MariaDB
MariaDB is a community-developed fork of the MySQL intended to remain free under the GNU GPL. The frontend component stores data into this DB.

The following steps follow (this document)(https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-lamp-amazon-linux-2.html).

### 1. Install
Install the lamp-mariadb10.2-php7.2 Amazon Linux Extras repository to get the latest versions of the LAMP MariaDB for Amazon Linux 2. PHP won't be used.
```
sudo amazon-linux-extras install lamp-mariadb10.2-php7.2
```
If you failed with 'Cannot allocate memory' error, it is probably because the chat/frontend component services are already running. Stop them and try again.

Now MariaDB installation is enabled. Use the yum install command to install MariaDB.
```
sudo yum install -y mariadb-server
```

### 2. Secure Server
The default installation of the MariaDB server has several features that are great for testing and development, but they should be disabled or removed for production servers. The mysql_secure_installation command walks you through the process of setting a root password and removing the insecure features from your installation.

1. Start the MariaDB server.
```
sudo systemctl start mariadb
```

2. Run mysql_secure_installation.
```
sudo mysql_secure_installation
```
 + a. When prompted, type a password for the root account.

   + Type the current root password. By default, the root account does not have a password set. Press Enter.

   + Type Y to set a password, and type a secure password twice. For more information about creating a secure password, see https://identitysafe.norton.com/password-generator/. Make sure to store this password in a safe place.

 + b. Type Y to remove the anonymous user accounts.
 + c. Type Y to disable the remote root login.
 + d. Type Y to remove the test database.
 + e. Type Y to reload the privilege tables and save your changes.

### 3. Enable boot startup
```
sudo systemctl enable mariadb
```

### 4. Create New App User
Avoid using root user, this user is used for access of the frontend.

Bring up MySQL CLI prompt.
```
mysql --user=root --password
```
Enter the password for the root user.

Create a new user 'apps'.
```
MariaDB [(none)]> CREATE USER 'apps' IDENTIFIED BY 'yourpassword';
```

Only allow access from localhost.
```
MariaDB [(none)]> GRANT USAGE ON *.* TO 'apps'@localhost IDENTIFIED BY 'yourpassword';
```

### 5. Create New Database and Grant Access to User
Create a new database 'aplacchat' which is going to be used by frontend.
```
MariaDB [(none)]> CREATE DATABASE `aplacchat`;
```

Grant all privileges to the user on the database.
```
MariaDB [(none)]> GRANT ALL privileges ON `aplacchat`.* TO 'apps'@localhost;
```
