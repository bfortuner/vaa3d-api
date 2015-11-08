from bigneuron_app import db
from bigneuron_app.jobs.models import Job
from bigneuron_app.job_items.models import JobItem
from bigneuron_app.clients import s3
from bigneuron_app.clients.constants import S3_INPUT_BUCKET, S3_OUTPUT_BUCKET

def get_user_input_filenames(user_id):
	return s3.get_all_files(S3_INPUT_BUCKET)

def create_job(filenames, user):
	job = Job(user.id, 1) #Status = CREATED
	db.session.add(job)
	db.session.commit()

	for f in filenames:
		job_item = JobItem(job.job_id, f, 1) #Status = CREATED
		db.session.add(job_item)
	db.session.commit()

	return job.job_id