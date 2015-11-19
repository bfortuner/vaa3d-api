## Vaa3D API

Backend python API for handling users requests from https://github.com/bfortuner/vaa3d-website

Endpoint: http://vaa3d-api-dev.elasticbeanstalk.com/

Email bfortuner@gmail.com for access keys and credentials

### Setup

Clone github repository:

```
$ git clone https://github.com/bfortuner/vaa3d-api.git
$ cd vaa3d-api
```

Setup virtualenv:
```
$ sudo easy_install pip
$ sudo pip install virtualenv
$ virtualenv venv
$ . venv/bin/activate
```

Now install the required modules:
```
$ pip install -r requirements.txt
$ pip install awsebcli
$ pip install --upgrade google-api-python-client
```

Create required ENV variables (add to ~/.bash_profile)
```
export VAA3D_AWS_ACCESS_KEY='accesskey'		
export VAA3D_AWS_SECRET_KEY='secretkey'
export VAA3D_CONFIG='TestConfig'
export VAA3D_DB_PASSWORD='yourdbkey'
export VAA3D_PATH='yourpathtoVaa3d'
```

Now you can launch the app:
```
$ python application.py
```
And point your browser to http://0.0.0.0:5000

Run the vaa3d script
```
$ python run_job_with_s3.py
```

### Deploy to Elastic Beanstalk

Deactivate your virtual env:
```
$ deactivate
```

Create EB app:
```
$ eb init
$ eb create
$ eb start
$ eb stop
```

Push code to EB:
```
$ eb deploy
```

### Worker Setup on EC2

Download Vaa3D
```
cd; 
wget http://home.penglab.com/proj/vaa3d/v3100/Vaa3D_CentOS_64bit_v3.100.tar.gz
gunzip Vaa3D_CentOS_64bit_v3.100.tar.gz
```

Crontab to Run Vaa3d jobs on EC2
```
* * * * * . $HOME/.bash_profile; /usr/bin/python /home/ec2-user/vaa3d-api/task_runner.py process_jobs &>> /home/ec2-user/cronlog.log
*/1 * * * * . $HOME/.bash_profile; /usr/bin/python /home/ec2-user/vaa3d-api/task_runner.py process_job_items &>> /home/ec2-user/cronlog.log
```

Bash_Profile on EC2
```
export VAA3D_DB_PASSWORD='your-db-password'
export VAA3D_PATH='/home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh'
export EDITOR="emacs"

export DISPLAY=":98"
Xvfb $DISPLAY >& Xvfb.log &
trap "kill $! || true" EXIT
```

Libraries required to deploy Vaa3D
```
sudo yum install emacs
sudo yum install git
sudo yum install freeglut
sudo yum install mesa-libGL-devel mesa-libGLU-devel
sudo yum install gcc-c++
sudo yum install libXrender-devel.x86_64
sudo yum install xorg-x11-server-Xvfb
```

Run Vaa3D Command (***Absolute file paths are important***)
```
$VAA3D_PATH -x vn2 -f app2 -i /home/ec2-user/ziptest2.tif -o /home/ec2-user/output.swc
```
**make sure the test data is good quality (will say job is killed)

Clone GitHub
```
git clone https://github.com/bfortuner/vaa3d-api
cd vaa3d-api
sudo pip install -r requirements.txt
```

Kill Processes by Pattern
```
pgrep -f vaa3d
pkill -f vaa3d
```

### Links and Tutorials:
* https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
* http://blog.uptill3.com/2012/08/25/python-on-elastic-beanstalk.html
* http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
* https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic
* https://gist.github.com/mjul/54c7c9e936588e713537 (RDS postgres config)

### Permissions:
Request access tokens and permissions from bfortuner@gmail.com

### Troubleshooting:

ERROR: Operation Denied. The security token included in the request is invalid.
Update AWS config file with latest access tokens
$ cat ~/.aws/config

Cannot start x server (EC2 RedHat)
* sudo yum install xorg-x11-server-Xvfb
* Add the following to ~/.bash_profile
```
export DISPLAY=":98"
Xvfb $DISPLAY >& Xvfb.log &
trap "kill $! || true" EXIT
```
