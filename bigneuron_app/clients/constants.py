import os
from bigneuron_app import application
from bigneuron_app.jobs.constants import OUTPUT_FILE_SUFFIXES

AWS_REGION = application.config['AWS_REGION']
AWS_ACCESS_KEY = application.config['AWS_ACCESS_KEY']
AWS_SECRET_KEY = application.config['AWS_SECRET_KEY']
VAA3D_USER_AWS_ACCESS_KEY = application.config['VAA3D_USER_AWS_ACCESS_KEY']
VAA3D_USER_AWS_SECRET_KEY = application.config['VAA3D_USER_AWS_SECRET_KEY']

S3_INPUT_BUCKET=application.config['S3_INPUT_BUCKET']
S3_OUTPUT_BUCKET=application.config['S3_OUTPUT_BUCKET']
S3_WORKING_INPUT_BUCKET=application.config['S3_WORKING_INPUT_BUCKET']

AWS_IAM_USER_LOGIN_LINK='https://vaa3d.signin.aws.amazon.com/console/s3'

DYNAMO_JOB_ITEMS_TABLE=application.config['DYNAMO_JOB_ITEMS_TABLE']
DYNAMO_READS_PER_SEC=2
DYNAMO_WRITES_PER_SEC=2

# Vaa3d Program Directory
# /Applications/vaa3d/vaa3d64.app/Contents/MacOS/vaa3d64
# /home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh
VAA3D_PATH=os.getenv('VAA3D_PATH', '/home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh')
VAA3D_DEFAULT_PLUGIN='Vaa3D_Neuron2'
VAA3D_DEFAULT_FUNC='app2'
VAA3D_DEFAULT_OUTPUT_SUFFIX=OUTPUT_FILE_SUFFIXES[VAA3D_DEFAULT_PLUGIN]

# Test Data
VAA3D_TEST_INPUT_FILE_1='smalltest.tif'
VAA3D_TEST_INPUT_FILE_2='smalltest.tif.zip'
VAA3D_TEST_INPUT_FILE_3='smalltestdir.zip'
VAA3D_TEST_INPUT_FILE_4='smalltestdir_nested.zip'


CREATE_JOB_JSON={
    "filenames": [
        "smalltest.tif"
    ],
    "emailAddress": "bfortuner@gmail.com",
    "outputDir": "oindoin",
    "jobType": "Neuron Tracing",
    "plugin": {
        "settings": {
            "params": {
                "channel": "1"
            }
        },
        "name": "Vaa3D_Neuron2",
        "method": "app2"
    }
}