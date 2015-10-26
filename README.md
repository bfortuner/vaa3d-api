## Vaa3D API

Backend python API for handling users requests from https://github.com/bfortuner/vaa3d-website

Endpoint: http://vaa3d-api-env-u4euvdicze.elasticbeanstalk.com/


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

To play with the app right away, you can use a local database. Edit ```config.py``` by commenting out the AWS URL and uncomment this line:
```
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
```
Next run:
```
$ python db_create.py
```
And the tables are created.  Now you can launch the app:
```
$ python application.py
```
And point your browser to http://0.0.0.0:5000


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

Links and Tutorials:
* https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
* http://blog.uptill3.com/2012/08/25/python-on-elastic-beanstalk.html
* http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
* https://realpython.com/blog/python/flask-by-example-part-2-postgres-sqlalchemy-and-alembic
* https://gist.github.com/mjul/54c7c9e936588e713537 (RDS postgres config)

Permissions:
Request access tokens and permissions from bfortuner@gmail.com

Troubleshooting:

ERROR: Operation Denied. The security token included in the request is invalid.
Update AWS config file with latest access tokens
$ cat ~/.aws/config

