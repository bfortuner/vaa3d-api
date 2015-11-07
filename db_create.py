from application import db
from application.models import Data
from application.jobs.models import Job, JobStatus
from application.jobs.constants import JOB_STATUS_TYPES
from application.job_items.models import JobItem, JobItemStatus
from application.job_items.constants import JOB_ITEM_STATUS_TYPES
from application.users.models import User
from application.users.constants import DEFAULT_IAM_USER, DEFAULT_EMAIL, ADMIN_EMAIL, ADMIN_IAM_USER

"""
DO NOT RUN THIS SCRIPT IN PROD IF DATABASE ALREADY HAS LIVE DATA!
"""

# Drop and recreate DB
db.drop_all()
db.create_all()

print "DB tables created"

# Load Default Users
admin_user = User(ADMIN_EMAIL, ADMIN_IAM_USER)
default_user = User(DEFAULT_EMAIL, DEFAULT_IAM_USER)
db.session.add(admin_user)
db.session.add(default_user)

print "User table loaded"

# Load Job Status Types
for status_str in JOB_STATUS_TYPES:
	job_status = JobStatus(status_str)
	db.session.add(job_status)

print "JobStatusType table loaded"

# Load Job Item Status Types
for status_str in JOB_ITEM_STATUS_TYPES:
	job_item_status = JobItemStatus(status_str)
	db.session.add(job_item_status)

print "JobItemStatusType table loaded"

# Insert Test Job
job = Job(User.query.filter_by(iam_username='vaa3d-admin').first().id, 1)
db.session.add(job)

print "Loaded test job data"

# Insert Test Job Items
job = Job.query.first()
job_item1 = JobItem(job.job_id, 'file1.tif', 1)
job_item2 = JobItem(job.job_id, 'file2.tif', 1)
db.session.add(job_item1)
db.session.add(job_item2)

print "Loaded test job item data"

db.session.commit()