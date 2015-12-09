from bigneuron_app.database import db, init_db
from bigneuron_app.jobs.models import Job, JobStatus
from bigneuron_app.jobs.constants import JOB_STATUS_TYPES
from bigneuron_app.job_items import job_item_manager
from bigneuron_app.job_items.models import JobItemStatus
from bigneuron_app.job_items.constants import JOB_ITEM_STATUS_TYPES
from bigneuron_app.users.models import User
from bigneuron_app.users.constants import DEFAULT_IAM_USER, DEFAULT_EMAIL, ADMIN_EMAIL, ADMIN_IAM_USER
from bigneuron_app.clients.constants import *
from bigneuron_app.clients import dynamo, sqs


"""
DO NOT RUN THIS SCRIPT IN ''PROD'' IF DATABASE ALREADY HAS LIVE DATA!
"""

# Drop and recreate DB
init_db()

print "DB tables created"

# Load Default Users
admin_user = User(ADMIN_EMAIL, ADMIN_IAM_USER)
default_user = User(DEFAULT_EMAIL, DEFAULT_IAM_USER)
db.add(admin_user)
db.add(default_user)
db.commit()

print "User table loaded"

# Load Job Status Types
for status_str in JOB_STATUS_TYPES:
	job_status = JobStatus(status_str)
	db.add(job_status)
db.commit()

print "JobStatusType table loaded"

# Load Job Item Status Types
for status_str in JOB_ITEM_STATUS_TYPES:
	job_item_status = JobItemStatus(status_str)
	db.add(job_item_status)
db.commit()

print "JobItemStatusType table loaded"

# Insert Test Job
job = Job(User.query.filter_by(iam_username=DEFAULT_IAM_USER).first().id, 1, 
		'testjob1', VAA3D_DEFAULT_PLUGIN, VAA3D_DEFAULT_FUNC, 1, VAA3D_DEFAULT_OUTPUT_SUFFIX)
db.add(job)
db.commit()

print "Loaded test job data"

# Insert Test Job Items
job = Job.query.first()

# Dynamo - Drop and recreate DB
dynamo_conn = dynamo.get_connection()
dynamo.drop_table(dynamo_conn, DYNAMO_JOB_ITEMS_TABLE)
dynamo.create_table(dynamo_conn, DYNAMO_JOB_ITEMS_TABLE, 'job_item_key', 'S')

# Dynamo - Insert Test Data
job_item_doc1 = job_item_manager.build_job_item_doc(job, VAA3D_TEST_INPUT_FILE_1)
job_item_doc2 = job_item_manager.build_job_item_doc(job, VAA3D_TEST_INPUT_FILE_2)
job_item_doc3 = job_item_manager.build_job_item_doc(job, VAA3D_TEST_INPUT_FILE_3)
job_item_doc4 = job_item_manager.build_job_item_doc(job, VAA3D_TEST_INPUT_FILE_4)

job_item_manager.create_job_item_doc(job_item_doc1)
job_item_manager.create_job_item_doc(job_item_doc2)
job_item_manager.create_job_item_doc(job_item_doc3)
job_item_manager.create_job_item_doc(job_item_doc4)

# Drop and Recreate SQS queues
sqs.drop_and_recreate_queue(SQS_JOB_ITEMS_QUEUE)

# Add job_items to SQS
job_item_manager.add_job_item_to_queue(job_item_doc1.job_item_key)
job_item_manager.add_job_item_to_queue(job_item_doc2.job_item_key)
job_item_manager.add_job_item_to_queue(job_item_doc3.job_item_key)
job_item_manager.add_job_item_to_queue(job_item_doc4.job_item_key)

print "Loaded test job item data"





