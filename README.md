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
export VAA3D_USER_AWS_ACCESS_KEY='accesskey'		
export VAA3D_USER_AWS_SECRET_KEY='secretkey'
export VAA3D_CONFIG='TestConfig'
export VAA3D_DB_PASSWORD='yourdbkey'
export VAA3D_PATH='yourpathtoVaa3d'
export TASK_RUNNER_PATH='xvfb-run python task_runner.py' #remove xvfb-run for local testing
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

### Setup Workers on EC2

Download Vaa3D
```
cd;
wget http://home.penglab.com/proj/vaa3d/v3100/Vaa3D_CentOS_64bit_v3.100.tar.gz
gunzip Vaa3D_CentOS_64bit_v3.100.tar.gz
tar -xvf Vaa3D_CentOS_64bit_v3.100.tar
```

Libraries required to deploy Vaa3D
```
sudo yum -y install emacs
sudo yum -y install git
sudo yum -y install freeglut
sudo yum -y install mesa-libGL-devel mesa-libGLU-devel
sudo yum -y install gcc gcc-c++
sudo yum -y install libpng12.x86_64 libXrender-devel.x86_64
sudo yum -y install xorg-x11-server-Xvfb
```

Add to Bash_Profile on EC2
```
export VAA3D_AWS_ACCESS_KEY='accesskey'		
export VAA3D_AWS_SECRET_KEY='secretkey'
export VAA3D_USER_AWS_ACCESS_KEY='accesskey'		
export VAA3D_USER_AWS_SECRET_KEY='secretkey'
export VAA3D_DB_PASSWORD='your-db-password'
export VAA3D_PATH='/home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh'
export TASK_RUNNER_PATH='xvfb-run python task_runner.py'

export DISPLAY=":98"

alias vaa3d='/home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh'
```

Download Test Data
```
aws s3 cp s3://vaa3d-test-data/smalltestdir.zip .
unzip smalltestdir.zip
```

Example Vaa3D Command
```
vaa3d -x vn2 -f app2 -i ~/testfilesdir/smalltest.v3dpbd
```
**make sure the test data is good quality (will say job is killed)
***Absolute file paths are important

Clone GitHub
```
git clone https://github.com/bfortuner/vaa3d-api
cd vaa3d-api
sudo pip install -r requirements.txt
---
pip freeze > requirements.txt (to add new reqs)
```

Command To Run Circus Workers
```
source ~/.bash_profile
cd ~/vaa3d-api
circusd --daemon circus.ini
```

Monitor Circus Workers
```
ps aux | grep task_runner
circus-top
circusctl
localhost:8080
circusctl quit
```

Kill Processes by Pattern
```
pgrep -f task_runner
pkill -f task_runner
```

### Testing

Running Unit Tests
```
python -m pytest tests/ (all tests)
python -m pytest -k filenamekeyword (specific tests)
python -m pytest tests/utils/test_sample.py (single test file)
python -m pytest tests/utils/test_sample.py::test_answer_correct (single test method)
python -m pytest --resultlog=testlog.log tests/ (send test output to file)
python -m pytest -s tests/ (print output to console)
```

### Docker

Setup for Mac
* https://docs.docker.com/engine/installation/mac/
* https://docs.docker.com/machine/

Docker Commands
```
docker-machine ls
docker-machine env default
eval "$(docker-machine env default)"
docker pull/push 647215175976.dkr.ecr.us-east-1.amazonaws.com/vaa3d:latest
cp dockerfiles/Dockerfile .
Update Dockerfile w TestConfig
docker build /path/to/Dockerfile/directory (or just . in in same directory)
docker images
docker run -d 647215175976.dkr.ecr.us-east-1.amazonaws.com/vaa3d:latest
docker ps
docker exec -t -i container_id bash
show envvariables (printenv)
docker rm -v $(docker ps -a -q) (remove all containers and volumes)
docker rmi $(docker images -q)
```

### ECS Setup (AWS Container Service)

Add Capacity to ECS Cluster via EC2
```
#http://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_container_instance.html
type amazon-ecs-optimized in the Search community AMIs
#!/bin/bash
echo ECS_CLUSTER=your_cluster_name >> /etc/ecs/ecs.config
```

###ECR Setup (AWS Container Repository)

```
#http://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_AWSCLI.html#AWSCLI_get-login
aws ecr get-login --region us-east-1
docker pull/push 647215175976.dkr.ecr.us-east-1.amazonaws.com/vaa3d:latest
```

### Links and Tutorials:
* https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
* http://blog.uptill3.com/2012/08/25/python-on-elastic-beanstalk.html
* http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
* https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic
* https://gist.github.com/mjul/54c7c9e936588e713537 (RDS postgres config)
* http://circus.readthedocs.org/en/latest/tutorial/step-by-step
* https://github.com/circus-tent/circus/tree/master/examples

### Permissions:
Request access tokens and permissions from bfortuner@gmail.com

### Troubleshooting:

ERROR: Operation Denied. The security token included in the request is invalid.
* Update AWS config file with latest access tokens
$ cat ~/.aws/config

Cannot start x server (EC2 RedHat)
* sudo yum install xorg-x11-server-Xvfb
* Add the following to ~/.bash_profile
```
export DISPLAY=":98"
Xvfb $DISPLAY >& Xvfb.log &
trap "kill $! || true" EXIT
```

Segmentation Fault. Job Killed
* File is too large, algo is too slow, or server does not have enough memory

File format not recognizes
* File may be corrupted. SCP from Mac --> Linux can cause this problem
