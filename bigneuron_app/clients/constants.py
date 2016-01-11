import os
from bigneuron_app import config

# AWS Config
AWS_REGION = config.AWS_REGION
AWS_ACCESS_KEY = config.AWS_ACCESS_KEY
AWS_SECRET_KEY = config.AWS_SECRET_KEY
VAA3D_USER_AWS_ACCESS_KEY = config.VAA3D_USER_AWS_ACCESS_KEY
VAA3D_USER_AWS_SECRET_KEY = config.VAA3D_USER_AWS_SECRET_KEY
AWS_IAM_USER_LOGIN_LINK='https://vaa3d.signin.aws.amazon.com/console/s3'

# S3 Config
S3_INPUT_BUCKET=config.S3_INPUT_BUCKET
S3_OUTPUT_BUCKET=config.S3_OUTPUT_BUCKET
S3_WORKING_INPUT_BUCKET=config.S3_WORKING_INPUT_BUCKET

# Dynamo Config
DYNAMO_JOB_ITEMS_TABLE=config.DYNAMO_JOB_ITEMS_TABLE
DYNAMO_READS_PER_SEC=config.DYNAMO_READS_PER_SEC
DYNAMO_WRITES_PER_SEC=config.DYNAMO_WRITES_PER_SEC

# ECS Config
ECS_CLUSTER=config.ECS_CLUSTER
ECS_JOB_ITEM_TASK=config.ECS_JOB_ITEM_TASK

# AWS Autoscaling Config
AUTOSCALING_GROUP=config.AUTOSCALING_GROUP

# SQS Config
SQS_JOB_ITEMS_QUEUE=config.SQS_JOB_ITEMS_QUEUE
SQS_JOB_ITEMS_DEAD_LETTER=config.SQS_JOB_ITEMS_DEAD_LETTER
SQS_JOBS_QUEUE=config.SQS_JOBS_QUEUE
SQS_MAX_RECEIVES=config.SQS_MAX_JOB_ITEM_RUNS
SQS_VISIBILITY_TIMEOUT=config.SQS_VISIBILITY_TIMEOUT

# Vaa3D Config
# /Applications/vaa3d/vaa3d64.app/Contents/MacOS/vaa3d64
# /home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh
VAA3D_PATH=os.getenv('VAA3D_PATH', '/home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh')
VAA3D_DEFAULT_PLUGIN='Vaa3D_Neuron2'
VAA3D_DEFAULT_FUNC='app2'
VAA3D_MIN_RUNTIME=config.VAA3D_MIN_RUNTIME #seconds
VAA3D_MAX_RUNTIME=config.VAA3D_MAX_RUNTIME
BUFFER_MULTIPLIER = config.VAA3D_TIMEOUT_BUFFER_MULTIPLE
BASE_BYTES_PER_SEC = 20000 #APP2 = 298891 bytes = 300KB / sec

# Test Data
VAA3D_TEST_INPUT_FILE_1='smalltest.tif'
VAA3D_TEST_INPUT_FILE_2='smalltest.tif.zip'
VAA3D_TEST_INPUT_FILE_3='smalltestdir.zip'
VAA3D_TEST_INPUT_FILE_4='corruptfile.tif'
VAA3D_TEST_INPUT_FILE_5='smalltest.v3dpbd'
VAA3D_TEST_INPUT_FILE_6='small.v3dpbd'
VAA3D_TEST_INPUT_FILE_7='zip_dir_w_single_zip_file.zip'


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